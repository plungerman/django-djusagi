from django.conf import settings
#from django.contrib import admin
from django.views.generic import RedirectView
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.views import static

from djauth.views import loggedout

from djusagi.calendar import views as cali_views
from djusagi.core import views as core_views
#from djusagi.plus import views as plus_views

import os

urlpatterns = [
    # home
    url(
        r'^$', core_views.home,
        name='home'
    ),
    # calendar
    url(
        r'^calendar/$', cali_views.index,
        name='calendar_home'
    ),
    # emailsettings
    url(
        r'^emailsettings/', include('djusagi.emailsettings.urls')
    ),
    # groups
    url(
        r'^groups/', include('djusagi.groups.urls')
    ),
    # django auth
    url(
        r'^accounts/login/$',auth_views.login,
        {'template_name': 'accounts/login.html'},
        name='auth_login'
    ),
    url(
        r'^accounts/logout/$',
        auth_views.logout,{
            'next_page': '{}accounts/loggedout/'.format(settings.ROOT_URL)
        },
        name='auth_logout'
    ),
    url(
        r'^accounts/loggedout/$',
        loggedout,{'template_name': 'accounts/logged_out.html'},
        name='auth_loggedout'
    ),
    url(
        r'^accounts/$', RedirectView.as_view(url=settings.ROOT_URL)
    )
]

# not ready for prime time
    # admin
    #(r'^admin/', include(admin.site.urls) ),
    #url(r'^static/(?P<path>.*)$', static.serve,
    #    {'document_root': os.path.join(os.path.dirname(__file__), 'static')}
    #),
    # admin/docs
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # google+
    #url(
    #    r'^plus/$', plus_views.index,
    #    name='plus_home'
    #),
    # OAuth2
    #url(
    #    r'^oauth2-callback', plus_views.auth_return,
    #    name='oauth2_callback'
    #),
    #url(
    #    r'^oauth2-callback', 'djusagi.core.views.oauth2_callback',
    #    name="oauth2_callback"
    #),
