from django.conf import settings
from django.shortcuts import render

from djusagi.reports.manager import ReportsManager

from djtools.decorators.auth import group_required


@group_required(settings.ADMINISTRATORS_GROUP)
def index(request):
    '''
    '''

    return render(
        request, 'reports/home.html', {}
    )


@group_required(settings.ADMINISTRATORS_GROUP)
def two_factor_auth(request):

    return render(
        request, 'reports/two_factor_auth.html', {
            'faculty':faculty, 'staff': staff, 'students': students
        }
    )

