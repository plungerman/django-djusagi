# -*- coding: utf-8 -*-
import os, sys, json

# env
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/data2/django_1.7/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djusagi.settings")

from django.conf import settings

from googleapiclient.discovery import build
#from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

import argparse
import httplib2

"""
Shell script...
"""

# set up command-line options
desc = """
Accepts as input an email address of a google domain super user
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-e", "--email",
    required=True,
    help="email address of user",
    dest="email"
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

    '''
    with open(settings.SERVICE_ACCOUNT_KEY) as f:
        private_key = f.read()
    credentials = SignedJwtAssertionCredentials(
        settings.CLIENT_EMAIL, private_key,
        scope='https://www.googleapis.com/auth/admin.directory.user',
        sub=email
    )
    '''

    with open(settings.SERVICE_ACCOUNT_JSON) as json_file:

        json_data = json.load(json_file)
        if test:
            print json_data
        credentials = SignedJwtAssertionCredentials(
            json_data['client_email'],
            json_data['private_key'],
            scope='https://www.googleapis.com/auth/admin.directory.user',
            private_key_password='notasecret',
            sub=email
        )

    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build("admin", "directory_v1", http=http)
    results = service.users().list(
        domain=email.split('@')[1],
        maxResults=10,
        orderBy='email', viewType='domain_public'
    ).execute()

    print results

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    email = args.email
    test = args.test

    print args

    sys.exit(main())

