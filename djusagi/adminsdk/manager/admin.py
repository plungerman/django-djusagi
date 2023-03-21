# -*- coding: utf-8 -*-

from django.conf import settings
from djusagi.core.utils import get_cred
from googleapiclient.discovery import build


class AdminManager:
    """Google admin manager class."""

    def __init__(self):
        """Obtain credentials from the API."""
        scopes = [
            #'https://www.googleapis.com/auth/apps.groups.settings',
            #'https://www.googleapis.com/auth/admin.directory.group',
            #'https://www.googleapis.com/auth/admin.directory.group.member',
            #'https://www.googleapis.com/auth/admin.directory.group.security',
            'https://www.googleapis.com/auth/admin.directory.user',
            'https://www.googleapis.com/auth/admin.directory.group',
            'https://www.googleapis.com/auth/admin.directory.group.member',

        ]

        # obtain the admin directory service account cred
        self.cred = get_cred(scopes)

    def service(self):
        while True:
            try:
                service = build(
                    u'admin',
                    u'directory_v1',
                    credentials=self.cred,
                )
            except Exception as error:
                print(error)
            else:
                break

        return service
