from django.conf import settings
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views

from djauth.views import loggedout

import os

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'djgroo.plus.views.index'),
    url(r'^oauth2callback', 'djgroo.plus.views.auth_return'),
    # auth
    url(
        r'^accounts/login',
        auth_views.login,{'template_name': 'accounts/login.html'},
        name='auth_login'
    ),
    url(
        r'^accounts/logout/$',
        auth_views.logout,{'next_page': '/djgroo/accounts/loggedout/'},
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
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'static')
    }),
    # admin
    (r'^admin/', include(admin.site.urls) ),
    # override user creation
    #(r'^admin/auth/user/add/', 'djauth.views.user_add'),
    # admin/docs
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
