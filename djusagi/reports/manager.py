from django.conf import settings
from django.core.cache import cache

from djusagi.core.utils import get_cred

from googleapiclient.discovery import build
from datetime import  timedelta

import datetime
import httplib2

class ReportsManager(object):

    def __init__(self, scope):
        # obtain the reports user cred
        self.cred = get_cred(settings.DOMAIN_SUPER_USER_EMAIL, scope)

    def service(self):
        while True:
            try:
                service = build(
                    'admin', 'reports_v1',
                    http=self.cred.authorize(httplib2.Http())
                )
            except Exception, e:
                pass
            else:
                break

        return service

    def user_usage(self, email, parameters, date=None):
        '''
        Retrieves a report which is a collection of properties / statistics
        for a user.

        Required: 1) a valid email address from the domain.
                  2) parameters e.g. accounts:is_2sv_enrolled,
                                     accounts:is_2sv_enforced

        SCOPE: https://www.googleapis.com/auth/admin.reports.usage.readonly
        '''

        # date must be at least two days prior to current date, otherwise
        # the API will reject that request
        if not date or date > datetime.date.today() - timedelta(2):
            date = (datetime.date.today() - timedelta(2)).strftime('%Y-%m-%d')

        service = self.service()

        results = service.userUsageReport().get(
            userKey=email,
            date=date,
            parameters = parameters
        ).execute()

        return results

