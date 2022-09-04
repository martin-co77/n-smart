import io
import os
import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock

sys.path.append(os.path.join(os.getcwd(), 'src'))
sys.path.append(os.getcwd())

from test.routes.test_fixtures import TestFixtures


class AuthTestCase(TestFixtures):

    @mock.patch('routes.auth.index.tempfile.NamedTemporaryFile')
    @mock.patch('routes.auth.index.Facials.post_recognizer', return_value=('martin', MagicMock()))
    def test_login(self, post_recognizer, temp_file):
        file = (io.BytesIO(b"test"), 'test.jpg')
        self.set_query_return.append({'id': 1})
        response = self.client.post('/api/auth', data={
            'photo': file
        }, headers={'Authorization': "Bearer test"})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(1, response.json.get('data').get('id'))
        self.assertGreater(len(response.json.get('data').get('token')), 10)
        self.assertTrue(post_recognizer.called)
        self.assertTrue(temp_file.called)


if __name__ == '__main__':
    unittest.main()
