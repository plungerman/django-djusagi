# -*- coding: utf-8 -*-

import requests
import sys

sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')

from django.conf import settings
from djusagi.groups.manager import GroupManager


def main():
    """Maintain facstaff group members."""
    # group settings manager
    gm = GroupManager()
    # retrieve all groups in the domain
    members = gm.group_members(settings.FACSTAFF_GROUP_EMAIL)
    response = requests.get(
        settings.API_FACSTAFF_URL,
        headers={'Cache-Control': 'no-cache'},
    )
    emails = []
    for email in response.text.splitlines():
        emails.append(email)
    for member in members:
        if member['email'] not in emails:
            print(member)


if __name__ == '__main__':
    sys.exit(main())
