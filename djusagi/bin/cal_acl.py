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


# set up command-line options
desc = """
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    '-e', '--email',
    required=True,
    help='email address of user',
    dest='email'
)

def main():
    """main function."""

    credentials = get_cred(email, 'calendar')
    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build('calendar', 'v3', http=http)

    page_token = None
    while True:
        acl = service.acl().list(calendarId=email).execute()
        for rule in acl['items']:
            print(rule)
            #print('%s: %s' % (rule['id'], rule['role']))
        page_token = acl.get('nextPageToken')
        if not page_token:
            break


if __name__ == '__main__':
    args = parser.parse_args()
    email = args.email

    print args

    sys.exit(main())

