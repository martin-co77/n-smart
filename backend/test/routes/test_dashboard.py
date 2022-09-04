import os
import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock

sys.path.append(os.path.join(os.getcwd(), 'src'))
sys.path.append(os.getcwd())

from test.routes.test_fixtures import TestFixtures


class DashboardTestCase(TestFixtures):

    def test_list(self):

        with mock.patch('routes.alarm.index.Authorizer.validate_token') as mk:
            response = self.client.get('/api/stat', headers={'Authorization': "Bearer test"})

        self.assertEqual(response.status_code, 200)
        body = response.json
        self.assertTrue(len(body.get('data').get('grammar')) > 0)
        self.assertTrue(len(body.get('data').get('intruders')) > 0)
        self.assertTrue(len(body.get('data').get('statistics')) > 0)
        self.assertTrue(len(body.get('data').get('users')) > 0)
        self.assertTrue(len(body.get('data').get('webhooks')) > 0)
        self.assertEqual(body.get('status_text'), 'success')


if __name__ == '__main__':
    unittest.main()
