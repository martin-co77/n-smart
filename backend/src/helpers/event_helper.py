from config import AppConfig
from devices.device import Device
from exception.not_found import NotFoundException
from helpers.Log import Log
from lib.mysql import MySQL
from services.devices import Devices
from services.recognition import Facials


class EventHelper:
    db: MySQL = None
    configuration: AppConfig = None
    devices: Devices = None

    def __init__(self, configuration: AppConfig, db: MySQL, devices: Devices):
        self.db = db
        self.configuration = configuration
        self.devices = devices

    @staticmethod
    def add_item_to_dict(dict_content, item):
        dict_content.update(item)
        return dict_content

    @staticmethod
    def get_user_by(table, db: MySQL, key, value):
        return db.set_query(f"SELECT `id` FROM `{table}` WHERE `{key}` = %s", (value,))

    def facial_event_recognizer(self, **kwargs):
        nodes = self._get_events('authorize')
        door = self.devices.get_device(self.configuration.DEFAULT_DEVICE.get('DOOR'))

        if len(nodes) < 1:
            return

        (subject_id, authorizer) = Facials(
            configuration=self.configuration,
            devices=self.devices
        ).recognize()

        user = self.get_user_by(
            self.configuration.TABLES.get('USER'),
            self.db,
            'username',
            subject_id
        )[0]

        nodes = map(lambda x: self.add_item_to_dict(x, {'user_id': user.get('id')}), nodes)
        if subject_id is not None and len(subject_id) > 1:
            door.initialize(nodes=nodes)

    """
    Respond to all webhook, sending out
    """
    def _get_events(self, hook_type: str):

        from services.event import Event
        event_type = Event.NAMES.get(hook_type, None)
        if event_type is None:
            raise NotFoundException(f'Hook type {hook_type} not found!')

        return self.db.set_query(
            f"SELECT id, name, url, event FROM {self.configuration.TABLES.get('WEBHOOK')} WHERE `event` = %s",
            (event_type,)
        )

    def insert_log(self, data):
        """
        Write log to the database
        :param data:
        :return:
        """
        log: Log = data.get('data')
        self.db.insert(log.TABLE, log.get_values)

    def trigger_speech(self, kwargs):
        """
        Trigger the device for a speech event
        :param kwargs:
        :return:
        """
        if kwargs is None or 'current_user' not in kwargs:
            return

        nodes = self._get_events('speech')

        if len(nodes) < 1:
            return

        nodes = map(lambda x: self.add_item_to_dict(x, {'user_id': kwargs['current_user']}), nodes)
        self.devices.get_device(self.configuration.DEFAULT_DEVICE.get('HTTP_DEVICE')).initialize(nodes);


