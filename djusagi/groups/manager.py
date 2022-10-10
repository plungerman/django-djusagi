# -*- coding: utf-8 -*-

import httplib2

from django.conf import settings
from django.core.cache import cache
from djusagi.core.utils import get_cred
from djusagi.adminsdk.manager.admin import AdminManager
from googleapiclient.discovery import build


class GroupManager(object):
    """Google groups manager."""

    def __init__(self):
        """Set up scope and auth credentials."""
        # scope
        scope = 'https://www.googleapis.com/auth/apps.groups.settings'
        # obtain the admin directory user cred
        self.cred = get_cred(settings.DOMAIN_SUPER_USER_EMAIL, scope)

    def service(self):
        """Establish the sevice connection."""
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
        """Returns all groups in the domain using the adminsdk api."""
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
        """Retrieves a group's settings from the groups settings api."""
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

    def group_owner(self, members):
        """Retrieves the owner of a group from the list of group members."""
        owners = []
        if members:
            for member in members:
                if member['role'] == 'OWNER':
                    owners.append(member)
                    break
        return owners

    def group_members(self, email):
        """Retrieves a group's member list from the admin sdk api."""
        key = 'group_members_{0}'.format(email)
        members = cache.get(key)
        if not members:
            members = []
            page_token = None
            # build our members list
            am = AdminManager()
            service = am.service()
            while True:
                results = service.members().list(
                    groupKey=email,
                    alt='json',
                    maxResults=200,
                    pageToken=page_token,
                ).execute()
                page_token = results.get('nextPageToken')
                for member in results.get('members'):
                    members.append(member)
                if not page_token:
                    break
            cache.set(key, members)
        return members

    def member_has(self, group, email):
        """Retrieves group member status."""
        am = AdminManager()
        service = am.service()
        return service.members().hasMember(
            groupKey=group,
            memberKey=email,
        ).execute()

    def member_get(self, group, email):
        """Retrieves group member if exists."""
        am = AdminManager()
        service = am.service()
        return service.members().get(
            groupKey=group,
            memberKey=email,
        ).execute()

    def member_insert(self, group, email, member_type):
        """Retrieves group member if exists."""
        am = AdminManager()
        service = am.service()
        body = {
            'email': email,
            'role': 'MEMBER',
            'type': member_type,
            'status': 'ACTIVE',
            'delivery_settings': 'ALL_MAIL',
        }
        response = service.members().insert(
            groupKey=group,
            body=body,
        ).execute()
        return response

    def member_delete(self, group, email):
        """Delete a member from group."""
        am = AdminManager()
        service = am.service()
        response = service.members().delete(
            groupKey=group,
            memberKey=email,
        ).execute()
        return response
