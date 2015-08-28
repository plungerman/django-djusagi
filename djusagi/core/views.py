from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from djusagi.core.models import CredentialsModel
from djusagi.core.utils import get_flow

from oauth2client import xsrfutil
from oauth2client.django_orm import Storage

import os

@login_required
def home(request):
    """
    Home page view
    """
    return render_to_response(
        "home.html",
        context_instance=RequestContext(request)
    )

@login_required
def oauth2_callback(request):
    #flow = get_flow(request.session["scope"])
    flow = get_flow("plus.me")
    val = xsrfutil.validate_token(
        settings.SECRET_KEY, request.REQUEST['state'], request.user
    )
    if not val:
        return  HttpResponseBadRequest()
        '''
        return render_to_response(
            'core/debug.html', {
                'req':request.REQUEST,'val':val,'key':settings.SECRET_KEY
            },
             context_instance=RequestContext(request)
        )
        '''
    credential = flow.step2_exchange(request.REQUEST)
    storage = Storage(CredentialsModel, 'user', request.user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
