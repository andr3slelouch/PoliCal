# from google_auth_oauthlib.flow import InstalledAppFlow
import configuration

# import pickle
# import httplib2
# from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# This code is based on https://github.com/egeldenhuys/csv-to-calendar

"""
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=scopes)
    credentials = flow.run_console()

    pickle.dump(credentials, open(
        configuration.get_file_location(output_path), "wb"))
"""


def get(output_path="GCal.pkl"):
    CALENDAR_NAME = "PoliCal"
    CLIENT_SECRET_FILE = configuration.get_file_location("client_secret.json")
    APP_NAME = "PoliCal"
    scopes = ["https://www.googleapis.com/auth/calendar"]

    store = Storage(configuration.get_file_location(output_path))
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, scopes)
        flow.user_agent = APP_NAME
        credentials = tools.run_flow(flow, store)
        print(
            "Credenciales almacenadas en" + configuration.get_file_location(output_path)
        )
    return credentials
