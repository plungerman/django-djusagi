# -*- coding: utf-8 -*-
import os, sys

# env
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djusagi.settings")

from django.conf import settings

from djusagi.reports.manager import ReportsManager

from djimix.core.database import get_connection
from djimix.core.database import xsql

import argparse
import logging
logger = logging.getLogger(__name__)

# set up command-line options
desc = """
    Accepts as input for parameter "who": faculty, staff, students
    and optional cache flag
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    '-w',
    '--who',
    required=True,
    help="'faculty','staff', or 'students'",
    dest='who',
)
parser.add_argument(
    '--cache',
    action='store_true',
    help="Check the cache first for the results?",
    dest='cache',
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test',
)


def main():
    """Obtain the data about who has two-factor authentication enabled."""

    if who in {'faculty', 'staff'}:
        where = '{0} IS NOT NULL'.format(who)
    elif who == 'students':
        where = 'student IS NOT NULL and student <> "incoming"'
    else:
        print("--who must be: 'faculty','staff', or 'students'")
        exit(-1)

    sql = """
        SELECT
            id, lastname, firstname,
            (TRIM(username) || '@carthage.edu') as email
        FROM
            provisioning_vw
        WHERE
            {0}
        ORDER BY
            lastname, firstname
    """.format(where)

    report_man = ReportsManager(
        scope='https://www.googleapis.com/auth/admin.reports.usage.readonly',
        cache=cache
    )

    total = 0
    count = 0
    email = None

    with get_connection() as connection:
        rows = xsql(sql, connection)
        user_list = rows.fetchall()
    for usr in user_list:
        if usr[3] != email:
            try:
                user = report_man.user_usage(
                    email=usr[3],
                    parameters='accounts:is_2sv_enrolled'
                )
                if user['usageReports'][0]['parameters'][0]['boolValue']:
                    count += 1
                    if test:
                        print("{0} {1}".format(
                            usr[3],
                            user['usageReports'][0]['parameters'][0]['boolValue'],
                        ))
                total += 1
            except Exception as error:
                if test:
                    print("[error] {0}".format(error))
                else:
                    print("[error] {0}".format(error))
                    #logger.info("fail: {0}".format(error))
        try:
            email = usr[3]
        except Exception as error:
            email = None
            print("[error] {0}".format(error))

    print("{0} out of {1}".format(count, total))


if __name__ == '__main__':

    args = parser.parse_args()
    who = args.who
    test = args.test
    cache = args.cache

    if test:
        print(args)

    sys.exit(main())
