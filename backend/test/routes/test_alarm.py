import sys
import os
from unittest import mock

sys.path.append(os.path.join(os.getcwd(), 'src'))
sys.path.append(os.getcwd())

import unittest
from test.routes.test_fixtures import TestFixtures


class AlarmTestCase(TestFixtures):

    def test_create_alarm_success(self):
        with mock.patch('routes.alarm.index.Authorizer.validate_token') as mk:
            response = self.client.post('/api/alarm', json={
                    'email': 'johndoe@gmail.com',
            }, headers={'Authorization': "Bearer test"})

        self.assertTrue(self.db.insert.called)
        self.assertEqual(response.status_code, 201)

    def test_create_alarm_failed(self):
        with mock.patch('routes.alarm.index.Authorizer.validate_token') as mk:
            response = self.client.post('/api/alarm', json={}, headers={'Authorization': "Bearer test"})

        self.assertTrue(self.db.insert.not_called)
        self.assertEqual(response.status_code, 400)

    def test_list_alarm(self):
        with mock.patch('routes.alarm.index.Authorizer.validate_token') as mk:
            response = self.client.get('/api/alarm', headers={'Authorization': "Bearer test"})

        self.assertTrue(self.db.set_query.called)
        self.assertEqual(response.status_code, 200)

    def test_delete_alarm(self):
        with mock.patch('routes.alarm.index.Authorizer.validate_token') as mk:
            response = self.client.delete('/api/alarm/1', headers={'Authorization': "Bearer test"})

        self.assertTrue(self.db.delete.called)
        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
