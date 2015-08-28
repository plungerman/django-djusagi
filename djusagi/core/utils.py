from django.conf import settings
from django.core.urlresolvers import reverse_lazy

from oauth2client.client import flow_from_clientsecrets

def get_flow(scope):
    redirect = "https://{}{}".format(
        settings.SERVER_URL, reverse_lazy("oauth2_callback")
    )
    return flow_from_clientsecrets(settings.CLIENT_SECRETS,
        scope='https://www.googleapis.com/auth/{}'.format(scope),
        redirect_uri=redirect
    )
