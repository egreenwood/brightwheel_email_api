from django.conf import settings
import requests
import json
from bs4 import BeautifulSoup


class EmailRequestService:
    def __init__(self, email_data):
        # convert data to instance
        self.to = email_data['to']
        self.sender = email_data['sender']
        self.to_name = email_data['to_name']
        self.sender_name = email_data['from_name']
        self.subject = email_data['subject']
        soup = BeautifulSoup(email_data['body'], 'html.parser')
        self.body = soup.get_text()  # extract text from html

    def send_email(self):
        # sets request params from config, calls appropriate mail server function
        response = None
        url = settings.MAIL_CONFIG[settings.MAIL_SERVER]['URL']
        api_key = settings.MAIL_CONFIG[settings.MAIL_SERVER]['API_KEY']
        if settings.MAIL_SERVER == settings.MAILGUN:
            response = self.send_email_with_mailgun(url, api_key)
        elif settings.MAIL_SERVER == settings.SENDGRID:
            response = self.send_email_with_sendgrid(url, api_key)
        else:
            raise Exception('invalid email server config')
        return response

    def send_email_with_mailgun(self, url, api_key):
        # makes email request with mailgun config
        auth = ('api', api_key)
        data = {
            'from': '%s <%s>' % (self.sender_name, self.sender),
            'to': '%s <%s>' % (self.to_name, self.to),
            'subject': self.subject,
            'text': self.body
        }
        return requests.post(url, data=data, auth=auth)

    def send_email_with_sendgrid(self, url, api_key):
        # makes email request with sendgrid config
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % api_key}
        data = {
            "personalizations": [{
                "to": [{"email": self.to}]
            }],
            "from": {"email": self.sender},
            "subject": self.subject,
            "content": [{
                "type": "text/plain",
                "value": self.body
            }]
        }
        return requests.post(url, data=json.dumps(data), headers=headers)
