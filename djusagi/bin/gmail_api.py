# -*- coding: utf-8 -*-

import django
import sys
import argparse

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

django.setup()


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

    message = render_to_string('test_email.html', {'data': 'boo'})
    mail_subject = '[Gmail API] Vinz Clortho, Keymaster of Gozer'
    mail = EmailMessage(
        mail_subject,
        message, frum,
        to=[email],
        reply_to=[settings.ADMINS[0][1]],
    )
    mail.content_subtype = "html"
    #email.attach(sample_file.file.name, sample_file.file.read(), 'application/pdf')
    mail.send()


if __name__ == '__main__':
    args = parser.parse_args()
    email = args.email
    test = args.test
    sys.exit(main())
