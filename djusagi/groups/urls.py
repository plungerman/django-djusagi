from django.conf.urls import patterns, url

urlpatterns = patterns('djusagi.groups.views',
    # search
    url(
        r'^search/$', 'search', name="groups_search"
    ),
    # home
    url(
        r'^$', 'index', name="groups_home"
    )
)
