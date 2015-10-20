#!/usr/bin/python

from django.conf import settings

from apiclient import errors
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow

import httplib2

# Copy your credentials from the console
CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET

# Check https://developers.google.com/admin-sdk/directory/v1/guides/authorizing
# for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/admin.directory.user'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# Run through the OAuth flow and retrieve credentials
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
authorize_url = flow.step1_get_authorize_url()
print 'Go to the following link in your browser: ' + authorize_url
code = raw_input('Enter verification code: ').strip()
credentials = flow.step2_exchange(code)

# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

directory_service = build('admin', 'directory_v1', http=http)

all_users = []
page_token = None
params = {'customer': 'carthage.edu'}

while True:
  try:
    if page_token:
      params['pageToken'] = page_token
    current_page = directory_service.users().list(**params).execute()

    all_users.extend(current_page['users'])
    page_token = current_page.get('nextPageToken')
    if not page_token:
      break
  except errors.HttpError as error:
    print 'An error occurred: %s' % error
    break

for user in all_users:
  print user['primaryEmail']
