# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.cache import cache

from googleapiclient.discovery import build
from google.oauth2 import service_account


def get_cred(scopes, account=None):
    """Establishes the proper credentials to access the Google API resource."""
    if not account:
        account = settings.SERVICE_ACCOUNT_JSON
    credentials = service_account.Credentials.from_service_account_file(
        account,
        scopes=scopes,
        subject=settings.DOMAIN_USER_EMAIL,
    )
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

'''
from oauth2client.client import flow_from_clientsecrets
from django.urls import reverse_lazy
def get_flow(scope):
    redirect = "https://{}{}".format(
        settings.SERVER_URL, reverse_lazy("oauth2_callback")
    )
    return flow_from_clientsecrets(settings.CLIENT_SECRETS,
        scope='https://www.googleapis.com/auth/{}'.format(scope),
        redirect_uri=redirect
    )
'''
