from django.conf import settings
from django.shortcuts import render

from djusagi.reports.manager import ReportsManager
from djtools.decorators.auth import group_required
from djzbar.utils.informix import do_sql

import collections
import logging
logger = logging.getLogger(__name__)

EARL = settings.INFORMIX_EARL

@group_required(settings.ADMINISTRATORS_GROUP)
def index(request):
    '''
    '''

    return render(
        request, 'reports/home.html', {}
    )


@group_required(settings.ADMINISTRATORS_GROUP)
def two_factor_auth(request):

    groups = collections.OrderedDict()
    sql = 'SELECT * FROM provisioning_vw WHERE '
    groups['staff'] = '{0} staff IS NOT NULL'.format(sql)
    groups['faculty'] = '{0} faculty IS NOT NULL'.format(sql)
    groups['students'] = '{0} student IS NOT NULL'.format(sql)

    report_man = ReportsManager(
        scope='https://www.googleapis.com/auth/admin.reports.usage.readonly'
    )
    data = []
    for n,v in groups.items():
        sql = '{} ORDER BY email'.format(v)
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
                    total += 1
                except Exception, e:
                    logger.info("{} fail: {}".format(n, email))

            email = u.email
        groups[n] = total
        groups['{}_ave'.format(n)] = 100 * count / total
        data.append(count)
        data.append(total - count)

    return render(
        request, 'reports/two_factor_auth.html', {
            'groups': groups,
            'data' :data
        }
    )

