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

"""
Fetch all users from the Google API for a given domain
and check for aliases
"""

# set up command-line options
desc = """
Obtain all aliases from all users in the domain
"""

EMAIL = settings.DOMAIN_SUPER_USER_EMAIL

parser = argparse.ArgumentParser(description=desc)

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

    credentials = get_cred(EMAIL, "admin.directory.user")
    http = httplib2.Http()

    service = build(
        "admin", "directory_v1", http=credentials.authorize(http)
    )

    user_list = []
    page_token = None
    while True:
        results = service.users().list(
            domain=EMAIL.split('@')[1],
            maxResults=100,
            pageToken=page_token,
            orderBy='familyName', viewType='domain_public'
        ).execute(num_retries=10)

        for r in results["users"]:
            user_list.append(r)

        page_token = results.get('nextPageToken')
        if not page_token:
            break

    for user in user_list:
        pmail = user.get('primaryEmail')
        if pmail:
            aliases = service.users().aliases().list(userKey=pmail).execute(
                num_retries=10
            )
            if aliases and aliases.get('aliases'):
                for alias in aliases.get('aliases'):
                    if alias.get('alias'):
                        print('{}|{}|{}|{}'.format(
                            user.get('name').get('familyName'),
                            user.get('name').get('givenName'),
                            user.get('primaryEmail'), alias.get('alias')
                        ))

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    test = args.test

    if test:
        print(args)

    sys.exit(main())

