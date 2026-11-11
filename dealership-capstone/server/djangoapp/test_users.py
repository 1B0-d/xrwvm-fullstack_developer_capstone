import json
import secrets

from django.contrib.auth.models import User
from django.test import TestCase


class UserManagementTests(TestCase):
    def post_json(self, url, data):
        return self.client.post(url, json.dumps(data), content_type='application/json')

    def test_registration_login_logout_and_duplicate(self):
        details = {'userName': 'student', 'password': secrets.token_urlsafe(24),
                   'firstName': 'First', 'lastName': 'Last', 'email': 'student@example.com'}
        response = self.post_json('/djangoapp/register', details)
        self.assertEqual(response.json()['status'], 'Authenticated')
        self.assertTrue(User.objects.get(username='student').check_password(details['password']))
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(self.post_json('/djangoapp/register', details).json()['error'], 'Already Registered')
        self.assertEqual(self.client.get('/djangoapp/logout').status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertNotIn('status', self.post_json('/djangoapp/login', {'userName': 'student', 'password': 'wrong'}).json())
        self.assertEqual(self.post_json('/djangoapp/login', {'userName': 'student', 'password': details['password']}).json()['status'], 'Authenticated')

    def test_invalid_request(self):
        self.assertEqual(self.post_json('/djangoapp/register', {}).status_code, 400)
        self.assertEqual(self.post_json('/djangoapp/login', {}).status_code, 400)
        self.assertEqual(self.client.get('/djangoapp/register').status_code, 405)
