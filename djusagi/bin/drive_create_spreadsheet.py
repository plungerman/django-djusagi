# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/data2/django_1.7/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djusagi.settings")

from django.conf import settings

from djusagi.core.utils import get_cred

from googleapiclient.discovery import build

import argparse
import httplib2

import gspread


# set up command-line options
desc = """
Fetches a spreadsheet or creates one if it does not exist.
Accepts as input an email address of a google domain user
and a filename. Option description is allowed.
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-e", "--email",
    required=True,
    help="email address of user",
    dest="email"
)
parser.add_argument(
    "-f", "--filename",
    required=True,
    help="name of the file to manage",
    dest="filename"
)
parser.add_argument(
    "-d", "--description",
    required=False,
    help="description of the new file if create",
    dest="description"
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

    scope = 'https://www.googleapis.com/auth/drive '
    scope += 'https://spreadsheets.google.com/feeds'

    credentials = get_cred(email, scope, settings.SERVICE_ACCOUNT_JSON)

    http = httplib2.Http()
    credentials.authorize(http)

    service = build( "drive", "v2", http=http )

    gc = gspread.authorize(credentials)

    try:
        wks = gc.open(filename).sheet1
        print "opened existing file: {}".format(filename)
    except:
        if not description:
            description = "{}: File created from API".format(filename),
        body = {
            'title': filename,
            'description': description,
            'mimeType': "application/vnd.google-apps.spreadsheet"
        }

        # Create a new blank Google Spreadsheet file in user's Google Drive
        google_spreadsheet = service.files().insert(body=body).execute()

        #wks = gc.open(filename).sheet1
        print "newly created file: {}".format(filename)


######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    email = args.email
    filename = args.filename
    description = args.description
    test = args.test

    if test:
        print args

    sys.exit(main())

