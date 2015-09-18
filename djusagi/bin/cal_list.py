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

from djusagi.core.utils import get_cred

from googleapiclient.discovery import build
#from apiclient.discovery import build

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

def main():
    """
    main function
    """
    service = build("calendar", "v3", http=get_cred(email,"calendar"))

    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print calendar_list_entry['summary']
            print calendar_list_entry['accessRole']
            print calendar_list_entry['id']
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

