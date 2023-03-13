from django.conf import settings
from django.shortcuts import render

from djusagi.reports.manager import ReportsManager
from djtools.decorators.auth import group_required
from djimix.core.database import get_connection
from djimix.core.database import xsql

import collections
import logging
logger = logging.getLogger(__name__)


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
        sql = '{0} ORDER BY username'.format(v)
        total = 0
        count = 0
        username = None
        with get_connection() as connection:
            user_list = xsql(sql, connection).fetchall()
            for user in user_list:
                if user[3] != username:
                    try:
                        member = report_man.user_usage(
                            email='{0}@carthage.edu'.format(user[3]),
                            parameters='accounts:is_2sv_enrolled',
                        )
                        if member['usageReports'][0]['parameters'][0]['boolValue']:
                            count += 1
                        total += 1
                    except Exception, e:
                        logger.info("{0} fail: {1}".format(user[3], e))
                username = user[3]
            groups[n] = total
            groups['{0}_ave'.format(n)] = 100 * count / total
            data.append(count)
            data.append(total - count)

    return render(
        request,
        'reports/two_factor_auth.html',
        {'groups': groups, 'data' :data},
    )
