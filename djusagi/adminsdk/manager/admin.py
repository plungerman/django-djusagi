from django.conf import settings

from djusagi.core.utils import get_cred

from googleapiclient.discovery import build

import httplib2

class AdminManager(object):

    def __init__(self):
        # scope
        scope =  'https://www.googleapis.com/auth/admin.directory.group '
        scope +=  'https://www.googleapis.com/auth/admin.directory.user '
        # obtain the admin directory service account cred
        self.cred = get_cred(settings.DOMAIN_SUPER_USER_EMAIL, scope)

    def service(self):
        while True:
            try:
                service = build(
                    "admin", "directory_v1",
                    http=self.cred.authorize(httplib2.Http())
                )
            except Exception, e:
                pass
            else:
                break

        return service
