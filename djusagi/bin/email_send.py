# -*- coding: utf-8 -*-

import base64
import sys
import argparse

from django.conf import settings
from email.mime.text import MIMEText
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests import HTTPError


# set up command-line options
desc = "Accepts as input an email address to which we will send a message."
parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    '-e', '--email',
    required=True,
    help='email address',
    dest='email',
)
parser.add_argument(
    '--test',
    action='store_true',
    help='Dry run?',
    dest='test',
)


def main():
    """Send an email to an email address through google API."""

    scopes = ["https://www.googleapis.com/auth/gmail.send",]
    account = settings.GMAIL_SERVICE_ACCOUNT_JSON
    frum = settings.DEFAULT_FROM_EMAIL

    if test:
        print(account)
        print(frum)

    credentials = service_account.Credentials.from_service_account_file(
        account,
        scopes=scopes,
        subject=settings.SERVER_MAIL,
    )

    service = build('gmail', 'v1', credentials=credentials)

    body = """
    <html>
    <body>
      <p>Who does <b>your</b> taxes.</p>
    </body>
    </html>
    """
    message = MIMEText(body, 'html')
    message['To'] = email
    message['From'] = frum
    message['Reply-To'] = frum
    message['Subject'] = '[Gmail API] Vinz Clortho, Keymaster of Gozer'
    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'raw': encoded_message}

    try:
        message = (service.users().messages().send(userId='me', body=create_message).execute())
        print(F'sent message to {message} Message Id: {message["id"]}')
    except HTTPError as error:
        print(F'An error occurred: {error}')
        message = None


if __name__ == '__main__':
    args = parser.parse_args()
    email = args.email
    test = args.test
    sys.exit(main())
