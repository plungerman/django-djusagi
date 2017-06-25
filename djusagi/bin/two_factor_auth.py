# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/data2/django_1.11/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djusagi.settings")

from django.conf import settings
from djusagi.core.utils import get_cred

from oauth2client.file import Storage
from googleapiclient.discovery import build

from datetime import timedelta

import argparse
import httplib2
import datetime


SCOPE = 'https://www.googleapis.com/auth/admin.reports.usage.readonly'
DATE = (datetime.date.today() - timedelta(2)).strftime('%Y-%m-%d')

# set up command-line options
desc = """
Accepts as input an email address
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-e", "--email",
    required=True,
    help="email address from the domain",
    dest='email'
)
parser.add_argument(
    "--test",
    action='store_true',
    help="Dry run?",
    dest="test"
)


def main():
    '''
    Check if a user has two factor authorization enabled on their account
    '''

    # storage for credentials
    storage = Storage(settings.STORAGE_FILE)
    # create an http client
    http = httplib2.Http()

    # obtain the admin directory user cred
    users_cred = storage.get()
    if users_cred is None or users_cred.invalid:
        users_cred = get_cred(settings.DOMAIN_SUPER_USER_EMAIL, SCOPE)
        storage.put(users_cred)
    else:
        users_cred.refresh(http)

    # build the service connection
    service = build(
        'admin', 'reports_v1', http = users_cred.authorize(http)
    )

    results = service.userUsageReport().get(
        userKey=email,
        date=DATE,
        parameters = 'accounts:is_2sv_enrolled,accounts:is_2sv_enforced'
    ).execute()

    print results
    print results['usageReports'][0]['parameters'][0]['boolValue']
    print results['usageReports'][0]['parameters'][1]['boolValue']


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

