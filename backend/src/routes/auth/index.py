from datetime import datetime
from flask import request
from routes.controller import Controller
from services.recognition import Facials
from services.response import Response
import jwt as jwt
import tempfile


class Authorization(Controller):

    def create_log(self, current_user: int, user_id: int, status):
        self.write_log('RECENT_LOGIN', 'Admin', 'Web', 'Login', current_user, user_id, status)

    def update_last_login(self, user):
        self.db.update(
            self.configuration.TABLES.get('USER'),
            {
                'last_login': datetime.now()
            },
            'id',
            int(user.get('id'))
        )

        self.create_log(user.get('id'), user.get('id'), True)

    def login(self):
        """
        Login
        :return:
        """
        response = Response()

        try:
            data = request.files

            if data is None or 'photo' not in data:
                return response.set('No auth information supplied', False, 401).jsonify()

            photo = data.get('photo')

            username = False

            with tempfile.NamedTemporaryFile() as tmp:
                tmp.write(photo.stream.read())
                username, data = (Facials(configuration=self.configuration, devices=self.devices)).post_recognizer(tmp.name)

            if username is False:
                return response.set('Invalid login', False, 401).jsonify()

            user = self.db.set_query(
                f"SELECT id, is_super, firstname, lastname, email, phone, last_login, picture FROM {self.configuration.TABLES.get('USER')} WHERE `username` = %s",
                (username,)
            )[0]

            user_id = user.get('id')
            if user_id is not None:
                token = jwt.encode(
                    {
                        'user': user_id
                    },
                    self.configuration.AUTH_TOKEN_SECRET,
                    algorithm='HS256'
                )
                self.configuration.CURRENT_USER.add(user_id)
                response_data = response.set('Success', True, 200, {
                    'token': token,
                    'id': user_id,
                    'firstname': user.get('firstname'),
                    'lastname': user.get('lastname'),
                    'picture': user.get('picture'),
                    'last_login': user.get('last_login'),
                    'is_super': user.get('is_super')
                }).jsonify()

                self.update_last_login(user)
                return response_data
        except Exception as e:
            return response.set(e.__str__(), False, 500).jsonify()
