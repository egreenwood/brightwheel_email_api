from django.conf import settings
from django.test import TestCase
from mock import patch
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.response import Response
import json
from models import EmailRequest
from email_request_service import EmailRequestService


class EmailViewTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    @patch.object(EmailRequestService, 'send_email')
    def test_create_email_request(self, send_email):
        # Ensure we can create a new email object.
        send_email.return_value = Response(status=status.HTTP_201_CREATED)
        url = '/email/'
        data = {'from': 'test@gmail.com', 'to': 'test', 'body': '', 'to_name': 'Sam'}
        response = self.client.post(url, data, format='json')

        # Requests with invalid fields should fail with helpful error messages
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'body': ['This field may not be blank.'],
            'to': ['Enter a valid email address.'],
            'subject': ['This field is required.'],
            'from_name': ['This field is required.']
        })

        data['body'] = '<p>Hello</p>'
        data['to'] = 'to@tomail.com'
        data['subject'] = 'Hello?'
        data['from_name'] = 'Eric'
        # Requests with valid fields should succeed
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content)['id'], EmailRequest.objects.get().id)

        # Email server requests that fail, return accepted response, and include email server errors
        send_email.return_value = Response('error', status=status.HTTP_400_BAD_REQUEST)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.json().keys()[0], 'email_server_errors')


class EmailRequestServiceTests(TestCase):
    def setUp(self):
        self.data = {
            'sender': 'george@gorilla.com',
            'from_name': 'George',
            'to': 'jane@godall.com',
            'to_name': 'Jane',
            'subject': 'Dinner tonight?',
            'body': '<p>I have some bananas for you!</p>',
        }

    def test_instance_parses_html(self):
        email_request = EmailRequestService(self.data)
        self.assertEqual(email_request.to, self.data['to'])
        self.assertEqual(email_request.to_name, self.data['to_name'])
        self.assertEqual(email_request.sender, self.data['sender'])
        self.assertEqual(email_request.sender_name, self.data['from_name'])
        self.assertEqual(email_request.subject, self.data['subject'])
        self.assertEqual(email_request.body, 'I have some bananas for you!')

    @patch.object(EmailRequestService, 'send_email_with_mailgun')
    @patch.object(EmailRequestService, 'send_email_with_sendgrid')
    def test_email_server_config(self, send_email_with_mailgun, send_email_with_sendgrid):
        with self.settings(MAIL_SERVER=settings.MAILGUN):
            email_request = EmailRequestService(self.data)
            email_request.send_email()

        with self.settings(MAIL_SERVER=settings.SENDGRID):
            email_request = EmailRequestService(self.data)
            email_request.send_email()

        with self.settings(MAIL_SERVER=''):
            self.assertRaises(Exception, email_request.send_email)

        email_request.send_email_with_mailgun.assert_called_once()
        email_request.send_email_with_sendgrid.assert_called_once()
