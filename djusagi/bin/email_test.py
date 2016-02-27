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
from oauth2client.client import SignedJwtAssertionCredentials
from oauth2client.file import Storage
from oauth2client.tools import run

import argparse
import httplib2

import gdata.gauth
import gdata.apps.emailsettings.client

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
    help="email address of administrative user",
    dest="email"
)
parser.add_argument(
    "-u", "--username",
    required=True,
    help="username of the account to search",
    dest="username"
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

    with open(settings.SERVICE_ACCOUNT_JSON) as json_file:

        json_data = json.load(json_file)
        #print json_data
        credentials = SignedJwtAssertionCredentials(
            json_data['client_email'],
            json_data['private_key'],
            scope='https://apps-apis.google.com/a/feeds/emailsettings/2.0/',
            access_type="offline",
            approval_prompt = "force",
            sub=email
        )

    storage = Storage(settings.STORAGE_FILE)

    storage.put(credentials)
    #credentials = storage.get()
    credentials.get_access_token()

    if test:
        print credentials.__dict__
        #print credentials.access_token

    http = httplib2.Http()
    auth = credentials.authorize(http)
    # refresh does not seem to work
    credentials.refresh(http)
    print credentials.__dict__

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    email = args.email
    test = args.test
    username = args.username

    #if test:
    #    print args

    sys.exit(main())

