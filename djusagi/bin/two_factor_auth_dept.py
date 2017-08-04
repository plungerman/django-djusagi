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

from djusagi.reports.manager import ReportsManager

from djzbar.utils.informix import do_sql

from directory.core import FACULTY_BY_DEPT, STAFF_BY_DEPT, STUDENTS_ALL

import collections
import argparse
import logging

logger = logging.getLogger(__name__)

EARL = settings.INFORMIX_EARL

# set up command-line options
desc = """
Accepts as input for parameter "who": faculty or staff
and optional cache flag
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-w", "--who",
    required=True,
    help="'faculty','staff', or 'students'",
    dest='who'
)
parser.add_argument(
    "--cache",
    action='store_true',
    help="Check the cache first for the results?",
    dest='cache'
)
parser.add_argument(
    "--test",
    action='store_true',
    help="Dry run?",
    dest="test"
)


def main():
    '''
    who has two-factor authentication enabled?
    '''

    if who == 'faculty':
        sql = '{} {}'.format(FACULTY_BY_DEPT, 'ORDER BY department, email')
    elif who == 'staff':
        sql = '{} {}'.format(
            STAFF_BY_DEPT, 'ORDER BY department, email'
        )
    elif who == 'students':
        sql = '{} {}'.format(STUDENTS_ALL, 'ORDER BY email')
    else:
        print "--who must be: 'faculty', 'staff', or 'students'"
        exit(-1)

    if test:
        print sql

    user_list = do_sql(sql, key=settings.INFORMIX_DEBUG, earl=EARL)

    dept_total = 0
    grand_total = 0
    dept_count = 0
    grand_count = 0
    email = None
    dept = None
    depts = collections.OrderedDict()

    report_man = ReportsManager(
        scope='https://www.googleapis.com/auth/admin.reports.usage.readonly',
        cache=cache
    )

    for u in user_list:

        if who != 'students' and test and u.department != dept:
            print u.department

        if dept and u.department != dept:
            depts[dept] = {
                'dept_count':dept_count, 'dept_total':dept_total
            }
            if test:
                print "{} has {} out of a total of {}".format(
                    dept, dept_count, dept_total
                )
            dept_count = 0
            dept_total = 0

        if u.email != email:
            try:
                user = report_man.user_usage(
                    email=u.email,
                    parameters='accounts:is_2sv_enrolled'
                )

                if user['usageReports'][0]['parameters'][0]['boolValue']:
                    dept_count += 1
                    grand_count += 1

                    if test:
                        print "{} {}".format(
                          u.email,
                          user['usageReports'][0]['parameters'][0]['boolValue']
                        )

                dept_total += 1
                grand_total += 1
            except Exception, e:
                if test:
                    print "error: {} {}".format(e, u.email)
                else:
                    logger.info("{} fail: {}".format(n, email))

            if test:
                print "Grand: {} out of {}".format(grand_count, grand_total)
                print dept

        email = u.email
        dept = u.department

    if test:
        for d in depts:
            print d, depts[d]


######################
# shell command line
######################

if __name__ == "__main__":

    args = parser.parse_args()
    who = args.who
    test = args.test
    cache = args.cache

    if test:
        print args

    sys.exit(main())

