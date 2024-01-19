# -*- coding: utf-8 -*-
import os, sys, json

from django.conf import settings

from googleapiclient.discovery import build
#from oauth2client.client import SignedJwtAssertionCredentials
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.file import Storage

import argparse
import httplib2


# set up command-line options
desc = """
Accepts as input an email address of a google domain super user
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-e", "--email",
    required=True,
    help="email address of administrative user",
    dest='email'
)
parser.add_argument(
    "--test",
    action='store_true',
    help="Dry run?",
    dest='test'
)

SCOPES = [
    'https://www.googleapis.com/auth/admin.directory.user',
    'https://www.googleapis.com/auth/admin.directory.user.security',
    'https://www.googleapis.com/auth/apps.groups.settings',
    'https://www.googleapis.com/auth/admin.directory.group',
    'https://www.googleapis.com/auth/admin.directory.group.member',
    'https://apps-apis.google.com/a/feeds/domain/',
    'https://apps-apis.google.com/a/feeds/groups/',
]


def main():
    global email

    with open(settings.SERVICE_ACCOUNT_JSON) as json_file:

        json_data = json.load(json_file)
        #print json_data
        #credentials = SignedJwtAssertionCredentials(
        credentials = ServiceAccountCredentials(
            json_data['client_email'],
            json_data['private_key'],
            scope = SCOPES,
            access_type='offline',
            approval_prompt = 'force',
            sub=email
        )
    storage = Storage(settings.STORAGE_FILE)
    print(storage.__dict__)
    storage.put(credentials)
    #credentials = storage.get()
    #credentials.get_access_token()

    print(credentials.__dict__)
    print(credentials.access_token)

    service = build("groupssettings", "v1", credentials=credentials)
    email = 'faculty-staff@carthage.edu'
    #gs = service.groups().get(groupKey=email)
    gs = service.groups().get(groupUniqueId=email).execute()
    print(gs.__dict__)
    '''
    group_list = service.groups.list()
    # cycle through the groups
    for group in group_list:
        print(group)
    gs = service.groups().get(
        groupKey=email,
        alt='json',
    ).execute()
    http = httplib2.Http()
    auth = credentials.authorize(http)
    # refresh does not seem to work
    credentials.refresh(http)
    print(credentials.__dict__)
    '''


if __name__ == "__main__":
    args = parser.parse_args()
    email = args.email
    test = args.test

    sys.exit(main())
