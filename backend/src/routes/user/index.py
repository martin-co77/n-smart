import datetime
import os
import uuid
from os.path import abspath
from config import AppConfig
from exception.invalid_input import InvalidInputException
from exception.not_found import NotFoundException
from helpers.event_helper import EventHelper
from lib.authorizer import Authorizer
from routes.controller import Controller
from flask import request
from services.recognition import Facials
from services.response import Response


class UserController(Controller):
    TABLE_NAME = AppConfig.TABLES.get('USER')

    @Authorizer.token_authorizer
    def create(self, current_user):
        """
        :param current_user:
        :return:
        """
        response = Response()

        try:
            body = request.form
            if body is None:
                raise InvalidInputException('Body is required', None)

            if 'firstname' not in body:
                raise InvalidInputException('First Name is required')

            if 'lastname' not in body:
                raise InvalidInputException('Last Name is required')

            if 'phone' not in body and 'email' not in body:
                raise InvalidInputException('Phone is required or Email is required')

            if request.files is None or 'photo' not in request.files:
                raise InvalidInputException('User avatar is required for authorization')

            username = body.get('firstname')+body.get('lastname')

            if len(EventHelper.get_user_by(self.TABLE_NAME, self.db, 'username', username)) > 1:
                raise InvalidInputException('User already exists. Please try with another user')

            user_data = dict({
                'firstname': body.get('firstname'),
                'lastname': body.get('lastname'),
                'phone': body.get('phone'),
                'email': body.get('email'),
                'username': username,
                'last_login': datetime.datetime.now()
            })

            file = request.files['photo']
            filename = uuid.uuid4().__str__()
            user_image_path = os.path.join(self.configuration.UPLOAD_DIR, filename)
            file.save(user_image_path)
            user_data.update({'picture': user_image_path})

            (Facials(configuration=self.configuration, devices=self.devices)).add_user(username, abspath(user_image_path))

            created = self.db.insert(self.TABLE_NAME, user_data)
            return response.\
                set('User created successfully!', True, 201, {'id': created}).\
                jsonify()

        except Exception as e:
            return response. \
                set(e.__str__(), False, 500, {}). \
                jsonify()

    @Authorizer.token_authorizer
    def update(self, id, current_user):
        """
        :param id:
        :param current_user:
        :return:
        """
        response = Response()
        body = request.form

        if current_user is None:
            raise NotFoundException("User id is required")

        user_data = dict({})

        if body is not None and 'firstname' in body:
            user_data.update({'firstname': body.get('firstname')})

        if body is not None and 'lastname' in body:
            user_data.update({'lastname': body.get('lastname')})

        if body is not None and 'phone' in body:
            user_data.update({'phone': body.get('phone')})

        if body is not None and 'email' in body:
            user_data.update({'email': body.get('email')})


        try:

            users = EventHelper.get_user_by(self.TABLE_NAME, self.db, 'id', current_user)

            if len(users) < 1:
                raise InvalidInputException('User does not exist')

            username = users[0].get('username')
            if request.files is not None and 'photo' in request.files:
                file = request.files['photo']
                user_image_path = os.path.join(self.configuration.UPLOAD_DIR, uuid.uuid4().__str__())
                file.save(user_image_path)
                user_data.update({'picture': user_image_path})
                (Facials(configuration=self.configuration, devices=self.devices)).add_user(username, abspath(user_image_path))

            self.db.update(self.TABLE_NAME, user_data, 'id', current_user)
            return response.set('success', True, 201, {'id': current_user}).jsonify()
        except Exception as e:
            return response.set(e.__str__(), False, 500).jsonify()

    @Authorizer.token_authorizer
    def index(self, current_user):
        """
        :param current_user:
        :return:
        """
        tables = self.configuration.TABLES

        response = Response()

        data = self.db.set_query(
            f"SELECT "
            f"(SELECT COUNT(id) FROM {tables.get('LOG')} u1 WHERE u1.user_associated = u.id AND u1.type=%s) as authorizations, "
            f"(SELECT COUNT(id) FROM {tables.get('LOG')} u1 WHERE u1.user_associated = u.id AND u1.type=%s) as alerts, "
            f"u.id, u.firstname, u.lastname, u.last_login, u.phone, u.email, u.picture FROM {self.TABLE_NAME} u",
            ('RECENT_LOGIN', 'INTRUSION')
        )

        return response.set('success', True, 200, data).jsonify()

    @Authorizer.token_authorizer
    def delete(self, current_user, id):
        """
        :param current_user:
        :param user_id:
        :return:
        """
        response = Response()

        data = self.db.delete(self.TABLE_NAME, 'id', id)
        return response.set('success', True, 201, data).jsonify()

