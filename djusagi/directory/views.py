from googleapiclient.discovery import build

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from djusagi.core.models import CredentialsModel
from djusagi.core.views import get_flow

from oauth2client import xsrfutil
from oauth2client.django_orm import Storage

import os
import logging
import httplib2

@login_required
def index(request):
    storage = Storage(CredentialsModel, 'user', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        request.session["scope"] = "admin.directory.user"
        FLOW = get_flow("admin.directory.user")
        FLOW.params['state'] = xsrfutil.generate_token(
            settings.SECRET_KEY, request.user
        )
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)


        service = build("admin", "directory_v1", http=http)
        results = service.users().list(
            customer='carthage.edu', maxResults=10,
            orderBy='email', viewType='domain_public'
        ).execute()

    return render(
        request, 'directory/index.html', {'users': users,}
    )

