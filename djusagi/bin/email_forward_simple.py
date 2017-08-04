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

from djusagi.core.utils import get_cred

from gdata.gauth import OAuth2TokenFromCredentials
from gdata.apps.emailsettings.client import EmailSettingsClient

import argparse
import httplib2

"""
Obtain the refresh token
"""

# set up command-line options
desc = """
Accepts as input an email address of a google domain super user
and a domain username e.g. jdoe
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

    global email

    # space separated list of authorized API scopes for this service account
    scope = 'https://apps-apis.google.com/a/feeds/emailsettings/2.0/'
    # create our email settings client
    client = EmailSettingsClient(domain=email.split('@')[1])
    # obtain our street cred
    credentials = get_cred(email, scope)
    # fetch our access token
    auth2token = OAuth2TokenFromCredentials(credentials)
    # authorize our client
    auth2token.authorize(client)

    forwarding = client.RetrieveForwarding(username=username)

    #print forwarding
    #print forwarding.__dict__
    print forwarding.property[1].value

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    email = args.email
    username = args.username
    test = args.test

    if test:
        print args

    sys.exit(main())

