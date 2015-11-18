from django.conf.urls import patterns, url

urlpatterns = patterns('djusagi.groups.views',
    # detail view for list and search
    url(
        r'^details/$', 'details', name="groups_search"
    ),
    # home
    url(
        r'^$', 'index', name="groups_home"
    )
)
