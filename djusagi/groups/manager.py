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

    def groups_list():
        """
        returns all groups in the domain
        """
        groups = cache.get("admin_sdk_groups_list")
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
            cache.set("admin_sdk_groups_list", groups, 60*60*24)

        return groups

    def group_settings(email):

        service = self.group_settings_service()
        while True:
            try:
                gs = service.groups().get(
                    groupUniqueId = email, alt='json'
                ).execute()
            except Exception, e:
                pass
            else:
                break

        return gs

    def group_members(email):
        service = self.admin_sdk_service()
        while True:
            try:
                members = service.members().list(
                    groupKey = email, alt='json'
                ).execute()
            except Exception, e:
                pass
            else:
                break

        return members

    def group_owner(members):
        if members.get("members"):
            for m in members.get("members"):
                if m["role"] == "OWNER":
                    owner = m
                    break
        else:
            owner = None
        return owner
