from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from googleapiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

import httplib2


@login_required
def index(request, email=None):

    if not email:
        email=settings.ADMINS[0][1]
    with open(settings.SERVICE_ACCOUNT_KEY) as f:
        private_key = f.read()

    credentials = SignedJwtAssertionCredentials(
        settings.CLIENT_EMAIL, private_key,
        'https://www.googleapis.com/auth/admin.directory.user',
        sub=email
    )

    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build("admin", "directory_v1", http=http)
    results = service.users().list(
        customer=email.split('@')[1], maxResults=10,
        orderBy='email', viewType='domain_public'
    ).execute()

    users = results.get('users', [])

    return render_to_response(
        'calendar/index.html', {'users': results,},
        context_instance=RequestContext(request)
    )

