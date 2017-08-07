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
and check for aliases
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

    credentials = get_cred(email, "gmail.settings.basic")
    http = httplib2.Http()
    service = build(
        "gmail", "v1", http=credentials.authorize(http)
    )
    aliases = service.users().settings().sendAs().list(
        userId=email
    ).execute()
    for alias in aliases.get('sendAs'):
        if alias.get('treatAsAlias') and alias.get('verificationStatus')=='accepted':
            print alias

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    email = args.email
    test = args.test

    if test:
        print args

    sys.exit(main())

