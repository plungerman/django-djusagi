# -*- coding: utf-8 -*-
import os, sys, json

# env
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/data2/django_1.7/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djusagi.settings")

from django.conf import settings

from googleapiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

import argparse
import httplib2

import feedparser
import untangle
import gdata.gauth
import gdata.apps.emailsettings.client

"""
Shell script...
"""

# set up command-line options
desc = """
Accepts as input an email address of a google domain super user
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-e", "--email",
    required=True,
    help="email address of administrative user",
    dest="email"
)
parser.add_argument(
    "-u", "--username",
    required=True,
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
    main function
    """

    with open(settings.SERVICE_ACCOUNT_JSON) as json_file:

        json_data = json.load(json_file)
        #print json_data
        credentials = SignedJwtAssertionCredentials(
            json_data['client_email'],
            json_data['private_key'],
            scope='https://apps-apis.google.com/a/feeds/emailsettings/2.0/',
            sub=email
        )

    credentials.get_access_token()

    if test:
        print credentials.access_token

    auth = gdata.gauth.OAuth2Token(
        credentials.client_id,#serviceEmail
        credentials.client_secret,#private key
        scope='https://apps-apis.google.com/a/feeds/emailsettings/2.0/',
        access_token=credentials.access_token,
        refresh_token=credentials.refresh_token,
        user_agent=credentials.user_agent
    )

    client = gdata.apps.emailsettings.client.EmailSettingsClient(
        domain=email.split('@')[1]
    )
    auth.authorize(client)

    '''
    #setting='forwarding'
    setting='delegation'
    uri = client.MakeEmailSettingsUri(username, setting)
    desired_class = gdata.apps.emailsettings.data.EmailSettingsDelegationFeed
    #desired_class = gdata.apps.emailsettings.data.EmailSettingsEntry
    delegates_xml = client.get_entry(
        uri=uri, desired_class=desired_class
    )
    print delegates_xml
    '''

    # these two lines do the same as above for 'forwarding'
    #forwarding = str(client.RetrieveForwarding(username=username))
    forwarding = client.RetrieveForwarding(username=username)
    #print forwarding.__dict__
    print forwarding.property[1]

    #print forwardings
    #obj = untangle.parse(forwarding)
    obj = untangle.parse(str(forwarding.property[1]))
    #obj = feedparser.parse(forwarding)
    print obj

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    email = args.email
    test = args.test
    username = args.username

    if test:
        print args

    sys.exit(main())

