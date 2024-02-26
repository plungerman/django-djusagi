# -*- coding: utf-8 -*-

import django
import sys
import argparse

from django.conf import settings
from djtools.utils.mail import send_mail


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
    frum = settings.DEFAULT_FROM_EMAIL
    subject = '[Gmail API] Vinz Clortho, Keymaster of Gozer'
    send_mail(
        None,
        [email],
        subject,
        frum,
        'test_email.html',
        'boo',
        reply_to=[settings.SERVER_EMAIL],
    )
    print(send_mail)


if __name__ == '__main__':
    args = parser.parse_args()
    email = args.email
    test = args.test
    sys.exit(main())
