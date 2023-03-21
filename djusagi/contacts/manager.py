# -*- coding: utf-8 -*-

import argparse
import datetime
import httplib2

from django.conf import settings
from django.core.cache import cache
from djusagi.core.utils import get_cred
from gdata.gauth import OAuth2TokenFromCredentials
from gdata.contacts import client as client_contacts
from gdata.contacts.client import ContactsQuery
from googleapiclient.discovery import build


class ContactsManager:

    def __init__(self, email, cache=True):
        # obtain our street cred
        scopes = ['https://www.google.com/m8/feeds/']
        credentials = get_cred(email, scopes)
        # initialise the client with an ad-hoc name
        self.client = client_contacts.ContactsClient(
            source=settings.CONTACTS_SOURCE
        )
        # fetch our access token
        auth2token = OAuth2TokenFromCredentials(credentials)
        # authorize our client
        auth2token.authorize(self.client)

    def save(self, contact):
        try:
            updated_contact = self.client.Update(contact)
        except gdata.client.RequestError, e:
            print e
            #if e.status == 412:
            #    # Etags mismatch: handle the exception.

    def contacts(self, max_results):

        query = ContactsQuery()
        query.max_results = max_results

        return self.client.GetContacts(q = query)

    def get_contact(self, earl):

        return self.client.GetContact(earl)

    def set_name(self, contact, name_list):

        # we use try/except because the name object is not always
        # complete
        try:
            contact.title.text = name_list[0]
        except Exception, e:
            print e
        try:
            contact.name.full_name.text = name_list[1]
        except Exception, e:
            print e
        try:
            contact.name.given_name.text = name_list[2]
        except Exception, e:
            print e
        try:
            contact.name.additionalName = name_list[3]
        except Exception, e:
            print e
        try:
            contact.name.family_name.text = name_list[4]
        except Exception, e:
            print e

        return contact

