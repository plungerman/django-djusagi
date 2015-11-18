from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response

from djusagi.adminsdk.manager.admin import AdminManager
from djusagi.groups.manager import GroupManager
from djusagi.core.utils import get_cred
from djusagi.groups.forms import SearchForm

from djtools.decorators.auth import group_required

from googleapiclient.discovery import build

import httplib2


@group_required(settings.ADMINISTRATORS_GROUP)
def index(request):
    """
    Fetch and display all of the google groups from a given domain
    """

    # group settings manager
    gm = GroupManager()
    # retrieve all groups in the domain
    group_list = gm.groups_list()
    # cycle through the groups
    for group in group_list:
        # fetch the group settings
        group["settings"] = gm.group_settings(group["email"])
        # fetch the group members
        group["members"] = gm.group_members(group["email"])
        # fetch the group owner
        group["owner"] = gm.group_owner(group["members"])

    return render_to_response(
        'groups/home.html', { 'groups': group_list },
        context_instance=RequestContext(request)
    )


@group_required(settings.ADMINISTRATORS_GROUP)
def details(request):

    members = False
    group = None
    email = None
    if request.method == "GET":
        email = request.GET.get("email")

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = cd["email"]
    else:
        form = SearchForm()

    if email:
        # group settings manager
        gm = GroupManager()

        service = gm.service()
        # build the groupsettings service connection
        try:
            group = service.groups().get(
                groupUniqueId=email, alt='json'
            ).execute()
        except Exception, e:
            if e.resp:
                group = e.resp.status
            else:
                group = e

    return render_to_response(
        'groups/details.html', {
            'email':email, 'form': form, 'group': group, 'members': members
        },
        context_instance=RequestContext(request)
    )

