import io
import os
import sys
from unittest import mock
from unittest.mock import MagicMock
from werkzeug.datastructures import FileStorage

sys.path.append(os.path.join(os.getcwd(), 'src'))
sys.path.append(os.getcwd())

import unittest
from test.routes.test_fixtures import TestFixtures


class UserTestCase(TestFixtures):

    @mock.patch('routes.user.index.Facials.post_recognizer', return_value=('martin', MagicMock()))
    @mock.patch('routes.user.index.Facials.add_user')
    def test_create_user_success(self, add_user_mock, post_recognizer_mock):

        file = FileStorage(
            stream=io.BytesIO(b'test'),
            filename="test_person1.jpeg",
            content_type="image/jpg",
        )
        file.write = MagicMock()
        with mock.patch('routes.alarm.index.Authorizer.validate_token') as mk:
            response = self.client.post('/api/user', data={
                'firstname': 'test',
                'lastname': 'testPerson',
                'phone': '0000222343',
                'photo': file
            }, headers={'Authorization': "Bearer test"},
               content_type="multipart/form-data"
           )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json.get('status_text') == 'User created successfully!')
        self.assertTrue(response.json.get('data').get('id'))

    def test_create_user_failed(self):
        with mock.patch('routes.user.index.Authorizer.validate_token') as mk:
            response = self.client.post('/api/user', data={
                'firstname': 'test',
                'lastname': 'testPerson',
                'phone': '0000222343',
            }, headers={'Authorization': "Bearer test"},
                                        content_type="multipart/form-data"
                                        )
        self.assertEqual(response.status_code, 500)
        self.assertTrue(response.json.get('status_text') == 'User avatar is required for authorization')

    def test_list_user(self):
        with mock.patch('routes.user.index.Authorizer.validate_token') as mk:
            response = self.client.get('/api/user', headers={'Authorization': "Bearer test"})

        self.assertGreater(len(response.json.get('data')), 0)
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        with mock.patch('routes.user.index.Authorizer.validate_token') as mk:
            response = self.client.delete('/api/user/1', headers={'Authorization': "Bearer test"})

        self.assertTrue(response.json.get('status_text') == 'success')
        self.assertIsNotNone(response.json.get('data'))
        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
