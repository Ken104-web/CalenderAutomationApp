import datetime as dt
import os.path


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else: 
            CURR_DIR = os.path.dirname(os.path.realpath(__file__))
            credential_file=str(CURR_DIR)+'/credentials.json'
            flow = InstalledAppFlow.from_client_secrets_file(
              credential_file, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    try:
        service = build("calendar", "v3", credentials=creds)

        now = dt.datetime.now().isoformat() + "Z" # 'Z'
        print ("Getting the upcoming 10 events")
        event_result = service.events().list(calendarId="primary",timeMin=now, maxResults=10,singleEvents=True, orderBy="startTime",).execute()
        events = event_result.get("items", [])

        if not events:
            print("No upcoming events found")
            return
        for i in events:
            start = i["start"].get("dateTime", i["start"].get("date"))
            print(start, i['summary'])

    except HttpError as error:
        print("AN error occured:", error)


if __name__ == "__main__":
    main()



