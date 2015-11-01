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

from googleapiclient.discovery import build
from oauth2client.file import Storage

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
    # storage for credentials
    storage = Storage(settings.STORAGE_FILE)
    # create an http client
    http = httplib2.Http()
    # scope
    scope =  'https://www.googleapis.com/auth/admin.directory.group '
    scope += 'https://www.googleapis.com/auth/apps.groups.settings'

    # obtain the admin directory user cred
    cred = get_cred(settings.DOMAIN_SUPER_USER_EMAIL, scope)
    # build the service connection
    service = build(
        "admin", "directory_v1", http=cred.authorize(http)
    )

    group_list = get_groups(service)

    """
    we initialise the Http() instance within the for loop
    in order to avoide the dreaded:

    'maximum recursion depth exceeded while calling a Python object'

    error, which is caused by reusing an Http() instance
    """
    for group in group_list:
        # build the service and fetch the group.
        # the build() and get() barf from time to time,
        # hence the try/except within a loop
        x = 1
        while True:
            http = httplib2.Http()
            try:
                service = build(
                    "groupssettings", "v1", http=cred.authorize(http)
                )
                g = service.groups().get(
                    groupUniqueId=group["email"], alt='json'
                ).execute()
            except Exception, e:
                print "[{}] {}) {}".format(datetime.datetime.today(), x, e)
                if x > 100:
                    break
                else:
                    x += 1
            else:
                break

        # build the service for fetching the group members.
        # the build() and get() barf from time to time,
        # hence the try/except within a loop
        x = 1
        while True:
            http = httplib2.Http()
            try:
                service = build(
                    "admin", "directory_v1", http=cred.authorize(http)
                )
                members = service.members().list(
                    groupKey = g["email"]
                ).execute()
            except Exception, e:
                print "[{}] {}) {}".format(datetime.datetime.today(), x, e)
                if x > 100:
                    break
                else:
                    x += 1
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

