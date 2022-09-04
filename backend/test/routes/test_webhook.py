import os
import sys
from unittest import mock

sys.path.append(os.path.join(os.getcwd(), 'src'))
sys.path.append(os.getcwd())

import unittest
from test.routes.test_fixtures import TestFixtures


class WebhookTestCase(TestFixtures):

    def test_list(self):
        with mock.patch('routes.webhook.index.Authorizer.validate_token') as mk:
            response = self.client.get('/api/webhook', headers={'Authorization': "Bearer test"})

        self.assertGreater(len(response.json.get('data')), 0)
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        with mock.patch('routes.webhook.index.Authorizer.validate_token') as mk:
            response = self.client.delete('/api/webhook/1', headers={'Authorization': "Bearer test"})

        self.assertTrue(response.json.get('status_text') == 'success')
        self.assertIsNotNone(response.json.get('data'))
        self.assertEqual(response.status_code, 201)

    def test_create_webhook_success(self):
        with mock.patch('routes.webhook.index.Authorizer.validate_token') as mk:
            response = self.client.post('/api/webhook', json={
                'name': 'test device',
                'url': 'http://192.168.1.39/authres',
                'event': 'speech',
            }, headers={'Authorization': "Bearer test"},
                                        content_type="multipart/form-data"
                                        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get('status_text'), 'Webhook created successfully!')
        self.assertTrue(response.json.get('data').get('id'))

    def test_create_webhook_failed(self):
        with mock.patch('routes.webhook.index.Authorizer.validate_token') as mk:
            response = self.client.post('/api/webhook', json={
                'name': 'test device',
                'url': 'http://192.168.1.39/authres',
                'event': 'speech1',
            }, headers={'Authorization': "Bearer test"},
                                        content_type="multipart/form-data"
                                        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json.get('status_text'), "Event not available. available are ['intruder', 'authorize', 'speech', 'motion', 'user', 'log']")
        self.assertFalse(response.json.get('status'))

    @mock.patch('main.EventHelper.trigger_speech')
    def test_incoming_webhook_json_success(self, speech_callback_mock):
        with mock.patch('routes.webhook.index.Authorizer.validate_token') as mk:
            response = self.client.post('/api/webhook/incoming', json={
                'data': 'Door Unlock',
                'event': 'speech',
            }, headers={'Authorization': "Bearer test"},
                                        content_type="multipart/form-data"
                                        )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json.get('status_text'), "success")
            self.assertTrue(response.json.get('status'))
            self.assertTrue(speech_callback_mock.called_with('Door Unlock'))

    @mock.patch('main.EventHelper.trigger_speech')
    def test_incoming_webhook_json_failed(self, speech_callback_mock):
        with mock.patch('routes.webhook.index.Authorizer.validate_token') as mk:
            response = self.client.post('/api/webhook/incoming', json={
                'data': 'Door Unlock',
                'event': 'speech1',
            }, headers={'Authorization': "Bearer test"},
                                        content_type="multipart/form-data"
                                        )

            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json.get('status_text'), "Event speech1 not available")
            self.assertFalse(response.json.get('status'))
            self.assertTrue(speech_callback_mock.not_called_with('Door Unlock'))

    @mock.patch('main.EventHelper.trigger_speech')
    def test_incoming_webhook_get_method_success(self, speech_callback_mock):
        with mock.patch('routes.webhook.index.Authorizer.validate_token') as mk:
            response = self.client.get('/api/webhook/incoming?data=Door Unlock&event=speech', headers={'Authorization': "Bearer test"},
                                        content_type="multipart/form-data"
                                        )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json.get('status_text'), "success")
            self.assertTrue(response.json.get('status'))
            self.assertTrue(speech_callback_mock.called_with('Door Unlock'))


if __name__ == '__main__':
    unittest.main()
