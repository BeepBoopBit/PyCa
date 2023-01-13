from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
# Reference: https://developers.google.com/identity/protocols/oauth2/scopes#calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']


class PyCa:
    def __init__(self):
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file(
                'token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        self.service = build('calendar', 'v3', credentials=self.creds)

    def createEvent(self, calendarId, event):
        # Reference: https://developers.google.com/calendar/api/guides/create-events#python
        # Reference: https://developers.google.com/calendar/api/v3/reference/events/insert
        event = self.service.events().insert(calendarId=calendarId, body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
    def getEvent(self):
        page_token = None
        events = self.service.events().list(calendarId='primary', pageToken=page_token).execute()
        for event in events['items']:
            print (event['summary'] + ":" + str(event['start']['dateTime']))
        page_token = events.get('nextPageToken')
        return [event['summary'], event['start']['dateTime']]

if __name__ == '__main__':
    newCalendar = PyCa()
    newCalendar.getEvent()
