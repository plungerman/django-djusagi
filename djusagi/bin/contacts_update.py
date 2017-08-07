# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djusagi.settings")

from django.conf import settings

from djusagi.contacts.manager import ContactsManager
from djusagi.adminsdk.manager.admin import AdminManager

import argparse

# set up command-line options
desc = """
    Accepts as input the email address of a google domain user
    whose contact information we should update for each user in the domain,
    and a python list with the values in quotes for the following fields
    in the contact object:

    title, name.fullName, name.givenName, name.additionalName, name.familyName

    e.g. ['Rosa Luxemburg', 'Rosa Luxemburg', 'Rosa', 'Maria', 'Luxemburg']
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-e", "--email",
    required=True,
    help="email address of user",
    dest="email"
)
parser.add_argument(
    "-n", "--names",
    type=str,
    nargs='*',
    required=True,
    help="python list of values for the new name",
    dest='names'
)
parser.add_argument(
    "--test",
    action='store_true',
    help="Dry run?",
    dest="test"
)

def main():
    '''
    Fetch all users from the Google API, go through their
    contacts, and update their contact record for the given
    email for the following fields:

    title
    fullName
    givenName
    familyName
    '''

    am = AdminManager()

    user_list = []
    page_token = None
    while True:
        results = am.service().users().list(
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

    count = 0
    for user in user_list:

        user_email = user["primaryEmail"]
        cm = ContactsManager(user_email)
        contacts = cm.contacts(settings.CONTACTS_MAX_RESULTS)

        # loop through all contacts in the user's collection
        for entry in contacts.entry:
            # loop through all emails for any given contact
            for e in entry.email:
                if e.address == email:
                    # loop through the various links
                    for l in entry.link:
                        if l.type == 'application/atom+xml' and l.rel == 'edit':
                            if test:
                                print user_email
                                print "\n{}".format(l.href)

                            contact = cm.get_contact(l.href)

                            if test:
                                print contact

                            if contact.name:
                                new_contact = cm.set_name(
                                    contact, names[0].split(',')
                                )
                                if test:
                                    print new_contact
                                cm.save(new_contact)
                                count += 1

    print "number of accounts updated: {}".format(count)


######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    email = args.email
    names = args.names
    test = args.test

    if test:
        print args

    sys.exit(main())

