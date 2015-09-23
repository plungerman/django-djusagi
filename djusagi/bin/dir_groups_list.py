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

from djusagi.core.utils import get_cred, get_group

from googleapiclient.discovery import build

import argparse
import httplib2

"""
Display all groups from a google domain
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
    fetch all the google groups from a given domain
    """

    credentials = get_cred(email, "admin.directory.group")

    http = httplib2.Http()
    credentials.authorize(http)

    service = build(
        "admin", "directory_v1", http=http)
    )

    groups = service.groups().list(
        domain=email.split('@')[1], maxResults=10
    ).execute()

    for g in groups["groups"]:
        print get_group(g, email)


######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    email = args.email

    print args

    sys.exit(main())

