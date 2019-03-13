# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')

from djusagi.core.utils import get_cred

from gdata.gauth import OAuth2TokenFromCredentials
from gdata.apps.emailsettings.client import EmailSettingsClient

import argparse
import httplib2
import os
import csv

# set up command-line options
desc = """
Accepts as input an email address of a google domain super user
and a CSV file to
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-e", "--email",
    required=True,
    help="email address of administrative user",
    dest="email"
)
parser.add_argument(
    "--file",
    required=True,
    help="path to CSV file",
    dest="phile"
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

    with open(phile, 'rb') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for r in reader:
            try:
                if '@' in r[0]:
                    forwarding = client.RetrieveForwarding(
                        username=r[0].split('@')[0]
                    ).property[1].value
                    if forwarding:
                        print("{],".format(forwarding))
            except:
                forwarding = None

    #print forwarding
    #print forwarding.__dict__
    print forwarding.property[1].value


######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    email = args.email
    phile = args.phile
    test = args.test

    if test:
        print args

    sys.exit(main())

