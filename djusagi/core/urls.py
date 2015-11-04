from django.conf import settings
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views

from djauth.views import loggedout
from djtools.views.dashboard import responsive_switch
import os

admin.autodiscover()

"""
    url(
        r'^oauth2-callback', 'djusagi.core.views.oauth2_callback',
        name="oauth2_callback"
    ),
"""
urlpatterns = patterns('',
    # home
    url(
        r'^$', 'djusagi.core.views.home',
        name="home"
    ),
    # calendar
    url(
        r'^calendar/$', 'djusagi.calendar.views.index',
        name="calendar_home"
    ),
    # emailsettings
    url(
        r'^emailsettings/', include('djusagi.emailsettings.urls')
    ),
    # groups
    url(
        r'^groups/', include('djusagi.groups.urls')
    ),
    # google+
    #url(
    #    r'^plus/$', 'djusagi.plus.views.index',
    #    name="plus_home"
    #),
    # OAuth2
    #url(
    #    r'^oauth2-callback', 'djusagi.plus.views.auth_return',
    #    name="oauth2_callback"
    #),
    # django auth
    url(
        r'^accounts/login',
        auth_views.login,{'template_name': 'accounts/login.html'},
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
        r'^accounts/loggedout',
        loggedout,{'template_name': 'accounts/logged_out.html'},
        name='auth_loggedout'
    ),
    url(
        r'^accounts/$', RedirectView.as_view(url=settings.ROOT_URL)
    ),
    # override mobile first responsive UI
    url(
        r'^responsive/(?P<action>[-\w]+)/',
        'responsive_switch', name="responsive_switch"
    ),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'static')
    }),
    # admin
    (r'^admin/', include(admin.site.urls) ),
    # admin/docs
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
