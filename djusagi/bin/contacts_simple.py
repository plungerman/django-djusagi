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
from gdata.contacts import client as client_contacts
from gdata.contacts import data

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

    # API scope
    scope = 'https://www.google.com/m8/feeds/'

    client = client_contacts.ContactsClient(
        source='Carthage_College_DJUsagi_ContactsClient'
    )

    #client.ClientLogin(email, password, client.source)

    # obtain our street cred
    credentials = get_cred(email, scope)
    # fetch our access token
    auth2token = OAuth2TokenFromCredentials(credentials)
    # authorize our client
    auth2token.authorize(client)

    # Note: The special userEmail value default can be used
    # to refer to the authenticated user.
    earl = 'https://www.google.com/m8/feeds/contacts/default/base/100914520372658838390'
    #earl = 'https://www.google.com/m8/feeds/contacts/default/full/100914520372658838390'
    #earl = 'https://www.google.com/m8/feeds/contacts/default/full?q=skirk@carthage.edu&v=3.0'
    #earl = 'https://www.google.com/m8/feeds/contacts/default/full/'

    #contact = client.GetContact(earl)
    contacts = client.GetContacts()

    #print contact
    print contacts
    for i, entry in enumerate(contacts.entry):

        try:
            print '\n%s %s' % (i+1, entry.name.full_name.text)
        except:
            print '\n%s %s' % (i+1, 'no full_name')
        if entry.content:
            print '    %s' % (entry.content.text)
        # Display the primary email address for the contact.
        for e in entry.email:
            if e.primary and e.primary == 'true':
                print '    %s' % (e.address)
        # Show the contact groups that this contact is a member of.
        for group in entry.group_membership_info:
            print '    Member of group: %s' % (group.href)
        # Display extended properties.
        for extended_property in entry.extended_property:
            if extended_property.value:
                value = extended_property.value
            else:
                value = extended_property.GetXmlBlob()
            print '    Extended Property - %s: %s' % (extended_property.name, value)


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

