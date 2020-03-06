# -*- coding: utf-8 -*-
import os
import sys

sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')

# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djusagi.settings')

from django.conf import settings

# informix environment
os.environ['INFORMIXSERVER'] = settings.INFORMIXSERVER
os.environ['DBSERVERNAME'] = settings.DBSERVERNAME
os.environ['INFORMIXDIR'] = settings.INFORMIXDIR
os.environ['ODBCINI'] = settings.ODBCINI
os.environ['ONCONFIG'] = settings.ONCONFIG
os.environ['INFORMIXSQLHOSTS'] = settings.INFORMIXSQLHOSTS
os.environ['LD_LIBRARY_PATH'] = settings.LD_LIBRARY_PATH
os.environ['LD_RUN_PATH'] = settings.LD_RUN_PATH

from djusagi.core.utils import get_cred
from djzbar.utils.informix import do_sql

from googleapiclient.discovery import build
#from apiclient.discovery import build

import argparse
import httplib2

EARL = settings.INFORMIX_EARL

# set up command-line options
desc = """
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    '-w', '--who',
    required=True,
    help="'faculty', 'staff', or 'student'",
    dest='who'
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test'
)


def main():
    """main function."""

    sql = """
        SELECT
            lastname, firstname, username
        FROM
            provisioning_vw
        WHERE
            {} is not null
        ORDER BY
            lastname, firstname
    """.format(who)

    if test:
        print("sql = {}".format(sql))
    else:
        user_list = do_sql(sql, key=settings.INFORMIX_DEBUG, earl=EARL)
        for user in user_list:
            email = '{0}@carthage.edu'.format(user.username)
            try:
                credentials = get_cred(email, 'calendar')
                http = httplib2.Http()
                http = credentials.authorize(http)
                service = build('calendar', 'v3', http=http)
            except Exception as error:
                print('{0}|{1}|{2}|Invalid email'.format(user.lastname, user.firstname, email))
                continue
            page_token = None
            domain = None
            while True:
                try:
                    acl = service.acl().list(calendarId=email).execute()
                except Exception:
                    print('{0}|{1}|{2}|No calendar'.format(user.lastname, user.firstname, email))
                    break
                for rule in acl['items']:
                    #print(rule)
                    #print('%s: %s' % (rule['id'], rule['role']))
                    # type == 'domain' value == 'carthage.edu'
                    #print(rule['scope']['type'])
                    #print(rule['scope']['value'])
                    if rule['scope']['type'] == 'domain':
                        domain = rule['role']
                        break
                page_token = acl.get('nextPageToken')
                if not page_token:
                    break
                # sometimes the google returns a shit tonne of pages that are just repeats
                if domain:
                    break
            if domain:
                print('{0}|{1}|{2}|{3}'.format(user.lastname, user.firstname, email, domain))
            else:
                print('{0}|{1}|{2}|No access'.format(user.lastname, user.firstname, email))


if __name__ == '__main__':
    args = parser.parse_args()
    test = args.test
    who = args.who.lower()

    if who not in {'student', 'faculty', 'staff'}:
        print("who must be: 'student', 'faculty', 'staff'\n")
        print("who = {}".format(who))
        exit(-1)
    print args

    sys.exit(main())

