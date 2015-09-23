from django.conf import settings
from django.core.urlresolvers import reverse_lazy

from djzbar.utils.informix import do_sql as do_esql

from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import SignedJwtAssertionCredentials

import json

EARL = settings.INFORMIX_EARL


def get_cred(email, scope):
    """
    Establishes the proper credentials to access the
    Google API resource
    """

    if scope[0:4] != "http":
        scope='https://www.googleapis.com/auth/{}'.format(scope),
    with open(settings.SERVICE_ACCOUNT_JSON) as json_file:
        json_data = json.load(json_file)
        credentials = SignedJwtAssertionCredentials(
            json_data['client_email'],
            json_data['private_key'],
            scope=scope,
            access_type="offline",
            approval_prompt = "force",
            token_uri='https://accounts.google.com/o/oauth2/token',
            sub=email
        )

    credentials.get_access_token()

    return credentials


def get_flow(scope):
    redirect = "https://{}{}".format(
        settings.SERVER_URL, reverse_lazy("oauth2_callback")
    )
    return flow_from_clientsecrets(settings.CLIENT_SECRETS,
        scope='https://www.googleapis.com/auth/{}'.format(scope),
        redirect_uri=redirect
    )


def get_group(g, email):

    service = build(
        "groupssettings", "v1", http=get_cred(email, "apps.groups.settings")
    )
    return service.groups().get(groupUniqueId=g["email"], alt='json').execute()


def get_users(sql):
    """
    Retrieve a list of users from Informix database
    """
    users = None
    objs = do_esql(sql,key=settings.INFORMIX_DEBUG,earl=EARL)
    if objs:
         users = objs.fetchall()
    return users

