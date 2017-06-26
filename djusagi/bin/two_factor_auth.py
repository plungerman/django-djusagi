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
from directory.core import FACULTY_ALPHA, STAFF_ALPHA


EARL = settings.INFORMIX_EARL

def main():
    '''
    '''

    report_man = ReportsManager(
        scope='https://www.googleapis.com/auth/admin.reports.usage.readonly'
    )

    user_list = do_sql(STAFF_ALPHA, key=settings.INFORMIX_DEBUG, earl=EARL)

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
                    print "{} {}".format(
                        u.email,
                        user['usageReports'][0]['parameters'][0]['boolValue']
                    )
            except Exception, e:
                print "error: {}".format(u.email)

        email = u.email

    print count

######################
# shell command line
######################

if __name__ == "__main__":

    sys.exit(main())

