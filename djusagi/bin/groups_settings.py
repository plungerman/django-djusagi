# -*- coding: utf-8 -*-

import sys
import argparse

from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build

# set up command-line options
desc = "Accepts as input an email address of a google group."
parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    '-g', '--group',
    required=True,
    help='email address of group',
    dest='group'
)
parser.add_argument(
    '--test',
    action='store_true',
    help='Dry run?',
    dest='test'
)


def main():
    scopes = [
        'https://www.googleapis.com/auth/admin.directory.user',
        'https://www.googleapis.com/auth/admin.directory.user.security',
        'https://www.googleapis.com/auth/apps.groups.settings',
        'https://www.googleapis.com/auth/admin.directory.group',
        'https://www.googleapis.com/auth/admin.directory.group.member',
        'https://apps-apis.google.com/a/feeds/domain/',
        'https://apps-apis.google.com/a/feeds/groups/',
    ]
    account = settings.SERVICE_ACCOUNT_JSON
    credentials = service_account.Credentials.from_service_account_file(
        account,
        scopes=scopes,
        subject=settings.DOMAIN_USER_EMAIL,
    )
    service = build(
        'groupssettings',
        'v1',
        credentials=credentials,
    )
    gs = service.groups().get(
        groupUniqueId=group,
        alt='json',
    ).execute()
    print(gs['whoCanLeaveGroup'])

    body = {
        'whoCanLeaveGroup': 'NONE_CAN_LEAVE',
    }
    response = service.groups().update(
        groupUniqueId=group,
        body=body,
    ).execute()
    print(response)


if __name__ == '__main__':
    args = parser.parse_args()
    group = args.group
    test = args.test
    if not settings.MEMBER_SYNC[group]:
        print('{0} is not a valid group at this time'.format(group))
        sys.ext(-1)
    sys.exit(main())
