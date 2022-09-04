from config import AppConfig
from lib.authorizer import Authorizer
from routes.controller import Controller
from routes.user.index import UserController
from services.response import Response
from flask import request


class AlarmController(Controller):
    TABLE_NAME = AppConfig.TABLES.get('ALARM')

    @Authorizer.token_authorizer
    def create(self, current_user):
        response = Response()

        try:
            body = request.get_json(force=True)
            if 'email' not in body and 'phone' not in body:
                return response.set('Either Email or Phone is required for alarm', False, 400).jsonify()

            db_body = dict({
                'user': current_user,
                'created': current_user
            })
            if 'email' in body and body.get('email') is not None:
                db_body.update({'email': body.get('email')})

            if 'phone' in body and body.get('phone') is not None:
                db_body.update({'phone': body.get('phone')})

            created = self.db.insert(self.TABLE_NAME, db_body)
            return response\
                .set('Alarm created successfully!', True, 201, {'id': created})\
                .jsonify()
        except Exception as e:
            return response.set(e.__str__(), False, 500, {}).jsonify()

    @Authorizer.token_authorizer
    def index(self, current_user):
        response = Response()

        try:
            data = self.db.set_query(
                f"SELECT a.id, a.phone, a.email, a.created_at, "
                f"u.firstname, u.lastname, u.last_login, u.phone, u.email, "
                f"u.picture FROM {self.TABLE_NAME} a INNER JOIN {UserController.TABLE_NAME} u on u.id = a.user",
                ()
            )
            return response.set('success', True, 200, data).jsonify()
        except Exception as e:
            return response.set(e.__str__(), False, 500, {}).jsonify()

    @Authorizer.token_authorizer
    def update(self, current_user):
        response = Response()
        return response.set('Not Implemented', False, 501).jsonify()

    @Authorizer.token_authorizer
    def delete(self, current_user, id):
        response = Response()

        data = self.db.delete(self.TABLE_NAME, 'id', id)
        return response.set('success', True, 201, data).jsonify()
