from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls import patterns, include, url


urlpatterns = patterns('djusagi.emailsettings.views',
    # home
    url(
        r'^$', RedirectView.as_view(url=settings.ROOT_URL)
    ),
    # search
    url(
        r'^search/$', 'search', name="emailsettings_search"
    ),
)
