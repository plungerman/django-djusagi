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

# informix environment
os.environ['INFORMIXSERVER'] = settings.INFORMIXSERVER
os.environ['DBSERVERNAME'] = settings.DBSERVERNAME
os.environ['INFORMIXDIR'] = settings.INFORMIXDIR
os.environ['ODBCINI'] = settings.ODBCINI
os.environ['ONCONFIG'] = settings.ONCONFIG
os.environ['INFORMIXSQLHOSTS'] = settings.INFORMIXSQLHOSTS
os.environ['LD_LIBRARY_PATH'] = settings.LD_LIBRARY_PATH
os.environ['LD_RUN_PATH'] = settings.LD_RUN_PATH


from djusagi.reports.manager import ReportsManager

from djzbar.utils.informix import do_sql
from directory.core import FACULTY_ALPHA, STAFF_ALPHA, STUDENTS_ALL

import argparse
import logging
logger = logging.getLogger(__name__)

EARL = settings.INFORMIX_EARL

# set up command-line options
desc = """
Accepts as input for parameter "who": faculty, staff, students
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
        sql = FACULTY_ALPHA
    elif who == 'staff':
        sql = STAFF_ALPHA
    elif who == 'students':
        sql = STUDENTS_ALL
    else:
        print "--who must be: 'faculty','staff', or 'students'"
        exit(-1)

    sql += ' ORDER BY email'

    report_man = ReportsManager(
        scope='https://www.googleapis.com/auth/admin.reports.usage.readonly',
        cache=cache
    )

    user_list = do_sql(sql, key=settings.INFORMIX_DEBUG, earl=EARL)

    total = 0
    count = 0
    email = None

    for u in user_list:

        if u.email != email:
            try:
                user = report_man.user_usage(
                    email=u.email,
                    parameters='accounts:is_2sv_enrolled'
                )
                if user['usageReports'][0]['parameters'][0]['boolValue']:
                    count += 1
                    if test:
                        print "{} {}".format(
                            u.email,
                            user['usageReports'][0]['parameters'][0]['boolValue']
                        )
                total += 1
            except Exception, e:
                if test:
                    print "error: {}".format(u.email)
                else:
                    logger.info("{} fail: {}".format(n, email))

        email = u.email

    if test:
        print "{} out of {}".format(count, total)


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

