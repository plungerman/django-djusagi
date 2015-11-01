from django.conf import settings
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import patterns, include, url

urlpatterns = patterns('djusagi.groups.views',
    # search
    url(
        r'^search/$', 'search', name="groups_search"
    ),
    # home
    url(
        r'^$', RedirectView.as_view(url=reverse_lazy('groups_search')),
        name="groups_home"
    )
)
