from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls import include, url

from djusagi.emailsettings import views


urlpatterns = [
    # home
    url(
        r'^$', RedirectView.as_view(url=settings.ROOT_URL)
    ),
    # search
    url(
        r'^search/$', views.search, name='emailsettings_search'
    ),
]
