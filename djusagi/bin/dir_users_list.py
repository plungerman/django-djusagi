# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')

from djusagi.core.utils import get_cred

from googleapiclient.discovery import build

import argparse
import httplib2

"""
Fetch all users from the Google API for a given domain
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
parser.add_argument(
    "--test",
    action='store_true',
    help="Dry run?",
    dest="test"
)

def main():
    """
    main function
    """

    credentials = get_cred(email, "admin.directory.user")
    http = httplib2.Http()

    service = build(
        "admin", "directory_v1", http=credentials.authorize(http)
    )

    user_list = []
    page_token = None
    while True:
        results = service.users().list(
            domain=email.split('@')[1],
            maxResults=500,
            pageToken=page_token,
            orderBy='email', viewType='domain_public'
        ).execute()

        for r in results["users"]:
            user_list.append(r)

        page_token = results.get('nextPageToken')
        if not page_token:
            break

    print "length of user_list: {}".format(len(user_list))
    for user in user_list:
        print user["primaryEmail"]
        #print user

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    email = args.email
    test = args.test

    print args

    sys.exit(main())

