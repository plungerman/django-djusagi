import os
import logging
import httplib2

from googleapiclient.discovery import build

from django.conf import settings
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from djusagi.plus.models import CredentialsModel

from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(
    os.path.dirname(__file__), '..', 'client_secrets.json'
)

FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/plus.me',
    redirect_uri=settings.OAUTH_REDIRECT_URI
)


@login_required
def index(request):
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(
            settings.SECRET_KEY, request.user
        )
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build("plus", "v1", http=http)
        activities = service.activities()
        activitylist = activities.list(
            collection='public', userId='me'
        ).execute()
        logging.info(activitylist)

    return render_to_response(
        'plus/welcome.html', {'activitylist': activitylist,},
        context_instance=RequestContext(request)
    )


@login_required
def auth_return(request):
    val = xsrfutil.validate_token(
        settings.SECRET_KEY, request.REQUEST['state'], request.user
    )
    if not val:
        #return  HttpResponseBadRequest()
        return render_to_response(
            'plus/debug.html', {
                'req':request.REQUEST,'val':val,'key':settings.SECRET_KEY
            },
             context_instance=RequestContext(request)
        )
    credential = FLOW.step2_exchange(request.REQUEST)
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect(settings.ROOT_URL)
