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
from djzbar.api.hr import get_users
from directory.core import FACULTY_ALPHA

from googleapiclient.discovery import build

import argparse

"""
Shell script...
"""

# set up command-line options
desc = """
Accepts as input a calendar ID as obtained from the google api
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-c", "--cid",
    required=True,
    help="Calendar ID",
    dest="cid"
)
parser.add_argument(
    "--test",
    action='store_true',
    help="Dry run?",
    dest="test"
)

EARL = settings.INFORMIX_EARL


def main():
    """
    Cycle through the users, obtain the user's calendar list, check
    for the calendar
    """

    user_list = get_users(FACULTY_ALPHA)
    cal_dict = { 'id': cid, "hidden": "False" }
    fails = []
    exists = []
    inserts = 1
    credentials = get_cred(email, "calendar")
    http = httplib2.Http()
    credentials.authorize(http)

    for user in user_list:
        email = user["email"]
        print email
        try:
            service = build("calendar", "v3", http=http)
            try:
                c = service.calendarList().get(calendarId=cid).execute()
                print "calendar already exists."
                #service.calendarList().delete(calendarId=cid).execute()
                exists.append(email)
            except:
                print "insert calendar"
                if not test:
                    service.calendarList().insert(body=cal_dict).execute()
                inserts += 1
        except:
            print "{} is not a valid email".format(email)
            fails.append(email)

    print "Total number of users: {}".format(len(user_list))
    print "Inserts = {}".format(inserts)
    print "Already exists ({}) = {}".format(len(exists), exists)
    print "Failures = {}".format(fails)

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    cid = args.cid
    test = args.test

    print args

    sys.exit(main())

