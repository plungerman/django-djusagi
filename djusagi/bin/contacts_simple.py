# -*- coding: utf-8 -*-
import sys

# env
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')

from djusagi.core.utils import get_cred

from gdata.gauth import OAuth2TokenFromCredentials
from gdata.contacts import client as client_contacts
from gdata.contacts.client import ContactsQuery

import argparse

"""
Obtain the refresh token
"""

# set up command-line options
desc = """
Accepts as input an email address of a google domain user
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-e", "--email",
    required=True,
    help="email address of a domain user",
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

    # API scope
    scope = 'https://www.google.com/m8/feeds/'

    client = client_contacts.ContactsClient(
        source='Carthage_College_DJUsagi_ContactsClient'
    )

    # obtain our street cred
    credentials = get_cred(email, scope)
    # fetch our access token
    auth2token = OAuth2TokenFromCredentials(credentials)
    # authorize our client
    auth2token.authorize(client)

    # Note: The special userEmail value default can be used
    # to refer to the authenticated user.
    #earl = 'https://www.google.com/m8/feeds/contacts/default/full/'

    query = ContactsQuery()
    query.max_results = 10000

    contacts = client.GetContacts(q = query)

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
    test = args.test

    if test:
        print args

    sys.exit(main())

