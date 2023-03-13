# django-djusagi
Dashboard manager for Google APIs

_Comma separated list of scopes for the service account_

http://www.google.com/m8/feeds,
https://apps-apis.google.com/a/feeds/emailsettings/2.0/,
https://mail.google.com/,
https://spreadsheets.google.com/feeds,
https://www.googleapis.com/auth/admin.directory.group,
https://www.googleapis.com/auth/admin.directory.group.member,
https://www.googleapis.com/auth/admin.directory.orgunit,
https://www.googleapis.com/auth/admin.directory.user,
https://www.googleapis.com/auth/admin.directory.user.alias,
https://www.googleapis.com/auth/admin.directory.user.readonly,
https://www.googleapis.com/auth/admin.directory.user.security,
https://www.googleapis.com/auth/admin.reports.audit.readonly,
https://www.googleapis.com/auth/admin.reports.usage.readonly,
https://www.googleapis.com/auth/apps.groups.settings,
https://www.googleapis.com/auth/calendar,
https://www.googleapis.com/auth/gmail.modify,
https://www.googleapis.com/auth/gmail.readonly,
https://www.googleapis.com/auth/gmail.settings.basic,
https://www.googleapis.com/auth/gmail.settings.sharing,
https://www.googleapis.com/auth/contacts.readonly

_admin console_

https://admin.google.com/

to manage API access, click on the "Security" icon, which takes you to:

https://admin.google.com/AdminHome#SecuritySettings:

click on the "show more" link, then click on "Advanced settings".
you will see one option for Authentication, which has a link to
"Manage API client access".

https://admin.google.com/AdminHome?chromeless=1#OGX:ManageOauthClients


copy the client name and paste it into the "client name" field. copy the
comma separated list above, add any new URLs, remove line breaks,
and paste into the 'One or More API Scopes' field. hit 'authorize'.

_API Manager_
https://console.developers.google.com/apis/dashboard?project=groups-settings&duration=PT1H

Create and manage service accounts, enable and disable Google APIs, etc.

_Migrations_
https://github.com/jhowe-sgs/mailman-to-google-groups
https://developers.google.com/admin-sdk/groups-migration/v1/guides/manage-email-migrations#group_migration_media_upload
