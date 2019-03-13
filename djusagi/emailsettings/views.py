from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import default_storage

from djusagi.core.utils import get_cred
from djusagi.emailsettings.forms import SearchForm

from djtools.decorators.auth import group_required

from gdata.gauth import OAuth2TokenFromCredentials
from gdata.apps.emailsettings.client import EmailSettingsClient

import os
import csv



@group_required(settings.ADMINISTRATORS_GROUP)
def search(request):

    forwarding = None
    emails = None
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():

            cd = form.cleaned_data
            # space separated list of authorized API scopes for
            # the service account
            scope = 'https://apps-apis.google.com/a/feeds/emailsettings/2.0/'
            # create our email settings client
            client = EmailSettingsClient(
                domain=settings.DOMAIN_SUPER_USER_EMAIL.split('@')[1]
            )
            # obtain our street cred
            credentials = get_cred(settings.DOMAIN_SUPER_USER_EMAIL, scope)
            # fetch our access token
            auth2token = OAuth2TokenFromCredentials(credentials)
            # authorize our client
            auth2token.authorize(client)
            if cd['username']:
                try:
                    forwarding = client.RetrieveForwarding(
                        username=cd["username"]
                    ).property[1].value
                except:
                    forwarding = None
            elif request.FILES.get('phile'):
                save_path = os.path.join(
                    settings.MEDIA_ROOT, 'files/emailsettings.csv'
                )
                path = default_storage.save(save_path, request.FILES['phile'])
                emails = []
                with open(path, 'rb') as f:
                    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
                    for r in reader:
                        try:
                            if '@' in r[0]:
                                forwarding = client.RetrieveForwarding(
                                    username=r[0].split('@')[0]
                                ).property[1].value
                                if forwarding:
                                    emails.append(forwarding)
                        except:
                            forwarding = None
            else:
                forwarding = 'Error'
    else:
        form = SearchForm()

    return render(
        request, 'emailsettings/search.html', {
            'form': form, 'forwarding': forwarding, 'emails': emails
        }
    )
