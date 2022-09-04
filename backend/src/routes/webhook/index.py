from datetime import datetime

from config import AppConfig
from exception.invalid_input import InvalidInputException
from lib.authorizer import Authorizer
from routes.controller import Controller
from services.event import Event
from services.response import Response
from flask import request


class WebhookController(Controller):
    TABLE_NAME = AppConfig.TABLES.get('WEBHOOK')

    @Authorizer.token_authorizer
    def index(self, current_user):
        response = Response()

        data = self.db.set_query(
            f"SELECT "
            f"w.id, w.name, w.url, w.event, w.created_at "
            f"FROM {self.TABLE_NAME} w ",
            ()
        )

        return response.set('success', True, 200, data).jsonify()

    @Authorizer.token_authorizer
    def update(self, current_user):
        response = Response()
        return response.set('Not Implemented', False, 501).jsonify()

    @Authorizer.token_authorizer
    def create(self, current_user):
        response = Response()
        try:

            body = request.get_json(force=True)

            if body is None or 'name' not in body:
                raise InvalidInputException('Name is required')

            if body is None or 'url' not in body:
                raise InvalidInputException('URL is required')

            if body is None or 'event' not in body:
                raise InvalidInputException('Event is required')

            if Event.NAMES.get(body.get('event')) is None:
                raise InvalidInputException(f'Event not available. available are {list(Event.NAMES.keys()).__str__()}')

            created = self.db.insert(self.TABLE_NAME, {
                'name': body.get('name', None),
                'url': body.get('url', None),
                'event': body.get('event', None),
                'registered_by': current_user,
                'created_at': datetime.now()
            })
            return response\
                .set('Webhook created successfully!', True, 201, {'id': created})\
                .jsonify()
        except Exception as e:
            return  response.set(e.__str__(), False, 500, {}).jsonify()

    @Authorizer.token_authorizer
    def delete(self, current_user, id):
        response = Response()

        data = self.db.delete(self.TABLE_NAME, 'id', id)
        return response.set('success', True, 201, data).jsonify()

    @Authorizer.webhook_authorizer
    def webhook(self, current_user):
        response = Response()
        try:
            body = request.get_json(force=True)
        except Exception as e:
            body = request.args

        try:
            if body is None or 'event' not in body or 'data' not in body:
                return response.set('Invalid data', False, 400).jsonify()
            self.configuration.event.call(body.get('event', None), data=body.get('data', None), current_user=current_user)
            return response.set('success', True, 200).jsonify()
        except Exception as e:
            return response.set(e.__str__(), False, 500).jsonify()


