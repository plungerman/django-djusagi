from django.conf import settings
from django.core.cache import cache

from djusagi.core.utils import get_cred
from djusagi.adminsdk.manager.admin import AdminManager

from googleapiclient.discovery import build

import httplib2

class GroupManager(object):

    def __init__(self):
        # scope
        scope = 'https://www.googleapis.com/auth/apps.groups.settings'
        # obtain the admin directory user cred
        self.cred = get_cred(settings.DOMAIN_SUPER_USER_EMAIL, scope)

    def service(self):
        while True:
            try:
                service = build(
                    "groupssettings", "v1",
                    http=self.cred.authorize(httplib2.Http())
                )
            except Exception, e:
                pass
            else:
                break

        return service

    def groups_list(self):
        """
        returns all groups in the domain using the adminsdk api.
        """
        key = "admin_sdk_groups_list"
        groups = cache.get(key)
        if not groups:
            groups = []
            page_token = None
            # build our group list
            am = AdminManager()
            service = am.service()
            while True:
                results = service.groups().list(
                    domain=settings.DOMAIN_SUPER_USER_EMAIL.split('@')[1],
                    maxResults=500,
                    pageToken=page_token
                ).execute()

                page_token = results.get('nextPageToken')

                for group in results["groups"]:
                    groups.append(group)
                if not page_token:
                    break
            # set cache to expire after 24 hours
            cache.set(key, groups, 86400)
        return groups

    def group_settings(self, email):
        """
        retrieves a group's settings from the groups settings api.
        """
        key = "group_settings_{}".format(email)
        gs = cache.get(key)
        if not gs:
            service = self.service()
            while True:
                try:
                    gs = service.groups().get(
                        groupUniqueId = email, alt='json'
                    ).execute()
                except Exception, e:
                    pass
                else:
                    break
            cache.set(key, gs)
        return gs

    def group_members(self, email):
        """
        retrieves a group's member list from the admin sdk api.
        """
        key = "group_members_{}".format(email)
        members = cache.get(key)
        if not members:
            am = AdminManager()
            service = am.service()
            while True:
                try:
                    members = service.members().list(
                        groupKey = email, alt='json'
                    ).execute()
                except Exception, e:
                    pass
                else:
                    break
            cache.set(key, members)
        return members

    def group_owner(self, members):
        """
        retrieves the owner of a group from the list of group members.
        """
        owner = None
        if members.get("members"):
            for m in members.get("members"):
                if m["role"] == "OWNER":
                    owner = m
                    break
        return owner
