from os.path import abspath

from config import AppConfig
from routes.alarm.index import AlarmController
from routes.auth.index import Authorization
from routes.controller import Controller
from routes.dashboard.index import Dashboard
from routes.user.index import UserController
from routes.webhook.index import WebhookController
from flask import send_from_directory


class Route:
    urls = None
    metds = []
    app = None
    configuration = None
    devices = None
    db = None

    def __init__(
            self,
            configuration: AppConfig,
            app, db,  **kwargs
    ):
        """
        :param configuration:
        :param app:
        :param db:
        :param kwargs:
        """
        self.configuration = configuration
        self.app = app
        self.db = db

        if kwargs is not None and 'devices' in kwargs:
            self.devices = kwargs['devices']

        self.urls = [UserController, AlarmController]
        self.append_route('index', '', 'GET')
        self.append_route('item', '<int:id>', 'GET')
        self.append_route('update', '<int:id>', 'PUT')
        self.append_route('create', '', 'post')
        self.append_route('delete', '<int:id>', 'DELETE')

    def append_route(self, name, url, method):
        """
        :param name:
        :param url:
        :param method:
        :return:
        """
        self.metds.append({'name': name, 'url': url, 'method': method})

    def add_route_methods(self, ctrlr: Controller):
        for mtd in self.metds:
            name = mtd.get('name', None)
            url = mtd.get('url', None)
            method = mtd.get('method', None)
            self.app.add_url_rule(f"/api/{ctrlr.TABLE_NAME}{'' if url == '' else '/'+url}", f"{ctrlr.TABLE_NAME} - {name}", getattr(ctrlr, name), methods=[method])

    def listen_webhook(self):
        webhook_ctlr = WebhookController(
            configuration=self.configuration,
            devices=self.devices,
            db=self.db
        )
        self.add_route_methods(webhook_ctlr)
        self.app.add_url_rule(
            f"/api/{webhook_ctlr.TABLE_NAME}/incoming",
            f"{webhook_ctlr.TABLE_NAME} - Incoming webhook",
            getattr(webhook_ctlr, 'webhook'),
            methods=['GET', 'POST'])

    def listen_authorization(self):
        authorization = Authorization(
            configuration=self.configuration,
            devices=self.devices,
            db=self.db
        )
        self.app.add_url_rule('/api/auth', 'auth', getattr(authorization, 'login'), methods=['POST'])

    def listen_dashboard(self):
        dashboard = Dashboard(
            configuration=self.configuration,
            devices=self.devices,
            db=self.db
        )
        self.app.add_url_rule('/api/stat', 'Dashboard', getattr(dashboard, 'index'), methods=['GET'])

    @staticmethod
    def static_file(path):
        return send_from_directory(abspath('files'), path)

    def setup(self):
        for cls in self.urls:
            ctrlr = cls(
                configuration=self.configuration,
                devices=self.devices,
                db=self.db
            )
            self.add_route_methods(ctrlr)

        self.listen_dashboard()
        self.listen_authorization()
        self.listen_webhook()
        self.app.add_url_rule('/files/<path:path>', 'Files', Route.static_file, methods=['GET'])
