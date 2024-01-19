# -*- coding: utf-8 -*-
import os, sys

# env
from django.conf import settings

from djusagi.core.utils import get_cred

from oauth2client.file import Storage
from googleapiclient.discovery import build
#from gdata.gauth import OAuth2TokenFromCredentials
#from gdata.apps.emailsettings.client import EmailSettingsClient

import argparse
import httplib2


# set up command-line options
desc = """
Accepts as input an email address of a google domain super user
and an optional username.
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-e", "--email",
    required=True,
    help="email address of administrative user",
    dest="email"
)
parser.add_argument(
    "--username",
    required=False,
    help="username of the account to search",
    dest="username"
)
parser.add_argument(
    "--test",
    action='store_true',
    help="Dry run?",
    dest="test"
)


def main():
    """
    Test the google api email settings, with the end goal of displaying
    'forwarding' information for any given account. try: mhamilton1 for POC.
    """

    global username
    global email
    global client

    if True:
        # storage for credentials
        storage = Storage(settings.STORAGE_FILE)
        # create an http client
        http = httplib2.Http()
        # email settings scope
        scope = 'https://apps-apis.google.com/a/feeds/emailsettings/2.0/'

        # obtain the admin directory user cred
        users_cred = storage.get()
        if users_cred is None or users_cred.invalid:
            users_cred = get_cred(email, "admin.directory.user")
            storage.put(users_cred)
        else:
            users_cred.refresh(http)

        # build the service connection
        service = build(
            "admin", "directory_v1", http = users_cred.authorize(http)
        )

        # fetch all of our users and put the results into a list
        user_list = []
        # intialize page_token
        page_token = None
        while True:
            results = service.users().list(
                domain=email.split('@')[1],
                maxResults=500,
                pageToken=page_token,
                orderBy='familyName', viewType='domain_public'
            ).execute()

            page_token = results.get('nextPageToken')
            user_list.append(results)
            if not page_token:
                break

        print("length of user_list: {}".format(len(user_list)))
        '''
        # we cycle through all of the users and fetch their
        # email settings, looking for the forwardTo key
        for users in user_list:

            for user in users["users"]:
                pmail = user["primaryEmail"]
                username = pmail.split('@')[0]
                given_name = user['name']['givenName']
                family_name = user['name']['familyName']
                # create our email settings client
                client = EmailSettingsClient(domain=email.split('@')[1])
                # obtain street cred
                credentials = get_cred(email, scope)
                auth2token = OAuth2TokenFromCredentials(credentials)
                auth2token.authorize(client)

                try:
                    forwarding = client.RetrieveForwarding(username=username)
                    if forwarding.property[1].value:
                        print("{}|{}|{}|{}".format(
                            family_name, given_name, pmail,
                            forwarding.property[1].value
                        ))
                except Exception as error:
                    print(("{0}|{1}|{2}|{3}".format(
                        family_name, given_name, pmail,
                        str(error)
                    )))
        '''


if __name__ == "__main__":
    args = parser.parse_args()
    email = args.email
    username = args.username
    test = args.test

    sys.exit(main())

