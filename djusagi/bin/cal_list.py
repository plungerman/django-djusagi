# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')

from djusagi.core.utils import get_cred

from googleapiclient.discovery import build
#from apiclient.discovery import build

import argparse
import httplib2

"""
Simple shell script to test the google calendar api
and display a list of all calendars for any given user account
"""

# set up command-line options
desc = """
Accepts as input an email address of a google domain user
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-e", "--email",
    required=True,
    help="email address of user",
    dest="email"
)

def main():
    """
    main function
    """

    credentials = get_cred(email, "calendar")
    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build("calendar", "v3", http=http)

    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print('summary{0}'.format(calendar_list_entry['summary']))
            print('accessRole{0}'.format(calendar_list_entry['accessRole']))
            print('id{0}'.format(calendar_list_entry['id']))
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    email = args.email

    print args

    sys.exit(main())

