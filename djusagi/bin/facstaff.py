# -*- coding: utf-8 -*-

import argparse
import requests
import sys

sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')

from django.conf import settings
from djusagi.groups.manager import GroupManager


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
    """Maintain facstaff group members."""
    # group settings manager
    gm = GroupManager()

    # retrieve all facstaff email from internal data source
    response = requests.get(
        settings.MEMBER_SYNC[group],
        headers={'Cache-Control': 'no-cache'},
    )

    # reconcile internal data with external data
    internal_emails = []
    for email in response.text.splitlines():
        try:
            member_get = gm.member_get(group, email)
        except Exception:
            if test:
                print('fetch member failed: {0}.'.format(email))
            member_get = None
        if member_get:
            internal_emails.append(email)
        # add to group if not a member
        member_type = 'USER'
        if not member_get:
            if 'carthage.edu' not in email:
                member_type = 'EXTERNAL'
            if test:
                print('adding member: {0}.'.format(email))
            result = gm.member_insert(group, email, member_type)
            if test:
                print('added member: {0}.'.format(result))

    # retrieve all members in the group
    members = gm.group_members(group)
    # remove members who are not part of internal data set
    for member in members:
        if member['email'] not in internal_emails and member['role'] != 'OWNER':
            if test:
                print('removing member: {0}.'.format(member))
            try:
                result = gm.member_delete(group, email)
            except Exception:
                if test:
                    print('delete member failed: {0}.'.format(member))
            if test and result:
                print('deleted member: {0}.'.format(result))


if __name__ == '__main__':
    args = parser.parse_args()
    group = args.group
    test = args.test
    if not settings.MEMBER_SYNC[group]:
        print('{0} is not a valid group at this time'.format(group))
        sys.ext(-1)
    sys.exit(main())
