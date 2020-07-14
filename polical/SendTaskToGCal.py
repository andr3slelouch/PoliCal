from apiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
import configuration
# import pickle
import datefinder
import pprint as pp
# import os
import httplib2
import get_GCal_Keys
from pathlib import Path
from datetime import timedelta, timezone


def create_event(start_time_str, summary, duration=1, attendees=None, description=None, location=None):
    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=duration)
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'datetime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/Guayaquil',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/Guayaquil',
        },
        'attendees': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    pp.pprint('''*** %r event added:
    With: %s
    Start: %s
    End:   %s''' % (summary.encode('utf-8'), attendees, start_time, end_time))
    return service.events().insert(calendarId='primary', body=event, sendNotifications=True).execute()


"""
scopes = ['https://www.googleapis.com/auth/calendar.events']

flow = InstalledAppFlow.from_client_secrets_file(
    configuration.get_file_location("client_secret.json"), scopes=scopes)
credentials = flow.run_console()

pickle.dump(credentials, open(
    configuration.get_file_location("GCal.pkl", "wb")))
"""
gcal_pkl = Path(configuration.get_file_location("GCal.pkl"))
# while(not gcal_pkl.is_file()):
# get_GCal_Keys.get(configuration.get_file_location("GCal.pkl"))
# credentials = pickle.load(
# open(configuration.get_file_location("GCal.pkl"), "rb"))
credentials = get_GCal_Keys.get()
http = credentials.authorize(httplib2.Http())
service = build("calendar", "v3", http=http)

result = service.calendarList().list().execute()

calendar_id = result['items'][0]['id']

result = service.events().list(calendarId=calendar_id).execute()
print(result['items'][0])
