# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/data2/django_1.11/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djusagi.settings")

from django.conf import settings
from djusagi.core.utils import get_cred

from oauth2client.file import Storage
from googleapiclient.discovery import build

import argparse
import httplib2

import logging

logger = logging.getLogger(__name__)

'''
'''

SCOPE = 'https://www.googleapis.com/auth/admin.reports.audit.readonly',

# set up command-line options
desc = """
Accepts as input an email address of a google domain super user
and a username.
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-e", "--email",
    required=True,
    help="email address of administrative user",
    dest='email'
)
parser.add_argument(
    "-u", "--username",
    required=False,
    help="username of the account to search",
    dest='username'
)
parser.add_argument(
    "--test",
    action='store_true',
    help="Dry run?",
    dest="test"
)


def main():
    """
    main function
    """

    global username
    global email
    global client

    if not username:
        username = 'all'
    else:
        username = '{}@carthage.edu'.format(username)

    # storage for credentials
    storage = Storage(settings.STORAGE_FILE)
    # create an http client
    http = httplib2.Http()

    # obtain the admin directory user cred
    users_cred = storage.get()
    if users_cred is None or users_cred.invalid:
        users_cred = get_cred(email, SCOPE)
        storage.put(users_cred)
    else:
        users_cred.refresh(http)

    # build the service connection
    service = build(
        "admin", "reports_v1", http = users_cred.authorize(http)
    )

    results = service.activities().list(
        userKey=username,
        applicationName='login',
        maxResults=10
    ).execute()

    activities = results.get('items', [])

    if not activities:
        print('No logins found.')
    else:
        print('Logins:')
        for activity in activities:
            print('{0}: {1} ({2})'.format(activity['id']['time'],
                activity['actor']['email'], activity['events'][0]['name']))


######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    email = args.email
    username = args.username
    test = args.test

    if test:
        print(args)

    sys.exit(main())

