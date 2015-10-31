from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse_lazy

from djzbar.utils.informix import do_sql as do_esql

from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import SignedJwtAssertionCredentials

import json
import httplib2

EARL = settings.INFORMIX_EARL


def get_cred(email, scope, service_account=None):
    """
    Establishes the proper credentials to access the
    Google API resource
    """

    if scope[0:4] != "http":
        scope='https://www.googleapis.com/auth/{}'.format(scope),
    if not service_account:
        service_account = settings.SERVICE_ACCOUNT_JSON
    with open(service_account) as json_file:
        json_data = json.load(json_file)
        credentials = SignedJwtAssertionCredentials(
            json_data['client_email'],
            json_data['private_key'],
            scope=scope,
            #access_type="offline",
            #approval_prompt = "force",
            token_uri='https://accounts.google.com/o/oauth2/token',
            sub=email
        )

    credentials.get_access_token()

    return credentials



def get_group(email, http):

    service = build(
        "groupssettings", "v1", http=http
    )
    return service.groups().get(groupUniqueId=email, alt='json').execute()


def get_groups(service):

    group_list = cache.get("admin_sdk_group_list")
    if not group_list:
        group_list = []
        page_token = None
        # build our group list
        while True:
            results = service.groups().list(
                domain=settings.DOMAIN_SUPER_USER_EMAIL.split('@')[1],
                maxResults=500,
                pageToken=page_token
            ).execute()

            page_token = results.get('nextPageToken')

            for group in results["groups"]:
                group_list.append(group)
            if not page_token:
                break
        # set cache to expire after 24 hours
        cache.set("admin_sdk_group_list", group_list, 60*60*24)
    return group_list


def get_flow(scope):
    redirect = "https://{}{}".format(
        settings.SERVER_URL, reverse_lazy("oauth2_callback")
    )
    return flow_from_clientsecrets(settings.CLIENT_SECRETS,
        scope='https://www.googleapis.com/auth/{}'.format(scope),
        redirect_uri=redirect
    )


