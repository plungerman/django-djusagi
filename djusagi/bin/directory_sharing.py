# -*- coding: utf-8 -*-
import sys

# env
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')

from django.conf import settings

from djusagi.core.utils import get_cred

from googleapiclient.discovery import build

import argparse
import httplib2


# set up command-line options
desc = "obtain all users who are suspended and have directory sharing enabled."

EMAIL = settings.DOMAIN_SUPER_USER_EMAIL

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    '--test',
    action='store_true',
    help='Dry run?',
    dest='test'
)


def main():
    """Main function."""

    credentials = get_cred(EMAIL, 'admin.directory.user')
    http = httplib2.Http()

    service = build('admin', 'directory_v1', http=credentials.authorize(http))

    user_list = []
    page_token = None
    while True:
        users = service.users().list(
            domain=EMAIL.split('@')[1],
            maxResults=100,
            pageToken=page_token,
            orderBy='familyName',
            #viewType='domain_public',
            viewType='admin_view',  # default
        ).execute(num_retries=10)

        for user in users['users']:
            user_list.append(user)

        page_token = users.get('nextPageToken')
        if not page_token:
            break

    print('email|suspended|name|directory')
    for user in user_list:
        if user.get('suspended') and user.get('includeInGlobalAddressList'):
        #if not user.get('includeInGlobalAddressList'):
            #print('{0}|{1}|{2}|{3}'.format(
            print('{0}|{1}|{2}'.format(
                user.get('primaryEmail'),
                #user.get('suspended'),
                user.get('name')['familyName'],
                user.get('name')['givenName'],
                #user.get('includeInGlobalAddressList'),
            ))


if __name__ == '__main__':
    args = parser.parse_args()
    test = args.test

    if test:
        print(args)

    sys.exit(main())

