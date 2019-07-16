from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
import time

actuator_url="http://192.168.1.100:3030"
meeting_room=actuator_url+"/meeting"

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    eventName=" "
    while True:

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='6u90hp5dcljnc59u87b7323on0@group.calendar.google.com', timeMin=now,
                                            singleEvents=True, orderBy='startTime', timeZone='Etc/Zulu',
                                            maxResults=10).execute()
        events = events_result.get('items', [])
    
        if not events:
            print('No upcoming events found.')
        for event in events:
            startTime = event['start'].get('dateTime')
            endTime = event['end'].get('dateTime')
            if startTime == None:
                print ("No time for this event")
            elif startTime < now and endTime > now and eventName != event['summary']: 
                print("Now"+now+" StartTime="+startTime+" EndTime="+endTime)
                print("Live event")
                requests.get(meeting_room+"/projector"+"/on")
                requests.get(meeting_room+"/blind"+"/off")
                requests.get(meeting_room+"/light"+"/off")
                eventName=event['summary']

        time.sleep(60)


if __name__ == '__main__':
    main()
