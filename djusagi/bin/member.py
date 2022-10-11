# -*- coding: utf-8 -*-

import argparse
import requests
import sys

from django.conf import settings
from djusagi.groups.manager import GroupManager

# set up command-line options
desc = "Accepts as input an email address of a google user."
parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    '-e', '--email',
    required=True,
    help='email address of user',
    dest='email'
)
parser.add_argument(
    '-g', '--group',
    required=True,
    help='email address of group',
    dest='group'
)
parser.add_argument(
    '-d',
    '--delete',
    action='store_true',
    help='Delete member?',
    dest='delete'
)
parser.add_argument(
    '-i',
    '--insert',
    action='store_true',
    help='Insert member?',
    dest='insert'
)
parser.add_argument(
    '--test',
    action='store_true',
    help='Dry run?',
    dest='test'
)


def main():
    """Group member manager."""
    # group settings manager
    gm = GroupManager()
    # retrieve member data
    try:
        member_get = gm.member_get(group, email)
        print(member_get)
    except Exception as error:
        member_get = None
        print('failed to get member: {0}'.format(email))
        print('error = {0}'.format(error))
    # delete member
    if member_get and delete:
        result = gm.member_delete(group, email)
        print(result)
    # insert member
    member_type = 'USER'
    if not member_get and insert:
        if 'carthage.edu' not in email:
            member_type = 'EXTERNAL'
        result = gm.member_insert(group, email, member_type)
        print(result)


if __name__ == '__main__':
    args = parser.parse_args()
    email = args.email
    group = args.group
    delete = args.delete
    insert = args.insert
    test = args.test
    test = args.test
    if not settings.MEMBER_SYNC.get(group):
        print('{0} is not a valid group at this time'.format(group))
        print(settings.MEMBER_SYNC)
        sys.exit(-1)
    sys.exit(main())
