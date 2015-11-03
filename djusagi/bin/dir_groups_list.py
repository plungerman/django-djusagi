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

from djusagi.core.utils import get_cred, get_groups, get_group
from djusagi.adminsdk.manager.admin import AdminManager
from djusagi.groups.manager import GroupManager

from googleapiclient.discovery import build

import argparse
import httplib2
import datetime
import json


# set up command-line options
desc = """
Display all groups from a google domain
"""

parser = argparse.ArgumentParser(description=desc)

def main():
    """
    fetch all the google groups from a given domain
    """

    print "[{}] Begin".format(datetime.datetime.today())

    am = AdminManager()
    # build the service connection
    service = am.service()

    group_list = get_groups(service)

    """
    we initialise the Http() instance within the for loop
    in order to avoide the dreaded:

    'maximum recursion depth exceeded while calling a Python object'

    error, which is caused by reusing an Http() instance
    """
    for group in group_list:
        # build the service and fetch the group.
        # service.groups().get() barfs from time to time,
        # hence the try/except within while a loop

        gm = GroupManager()
        service = gm.service()

        while True:
            try:
                g = service.groups().get(
                    groupUniqueId=group["email"], alt='json'
                ).execute()
            except Exception, e:
                print "[{}] {}".format(datetime.datetime.today(), e)
            else:
                break

        # fetch the group members.
        # get() barfs from time to time,
        # hence the try/except within a while loop
        while True:
            service = am.service()
            try:
                members = service.members().list(
                    groupKey = g["email"]
                ).execute()
            except Exception, e:
                print "[{}] {}".format(datetime.datetime.today(), e)
            else:
                break

        #print(json.dumps(members, indent=4))
        if members.get("members"):
            for m in members.get("members"):
                if m["role"] == "OWNER":
                    owner_email = m["email"]
                    break
        else:
            owner_email = None

        print u"{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(
            group["name"], owner_email, g["email"], g["whoCanJoin"],
            g["whoCanViewGroup"] , g["whoCanViewMembership"],
            g["whoCanPostMessage"], g["membersCanPostAsTheGroup"],
            g["whoCanContactOwner"], g["whoCanInvite"]
        ).encode("utf-8")

    print "[{}] End".format(datetime.datetime.today())

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()

    sys.exit(main())

