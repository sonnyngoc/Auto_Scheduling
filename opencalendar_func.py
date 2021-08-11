import datetime, json, pytz
import pickle
import os.path
import httplib2
from pytz import timezone
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# SCOPES = ['https://www.googleapis.com/auth/calendar']
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
# SCOPES = ['https://www.googleapis.com/auth/calendar']



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


    # This code is to fetch the calendar ids shared with me
    # Src: https://developers.google.com/google-apps/calendar/v3/reference/calendarList/list
    
    page_token = None
    calendar_ids = []
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if "@nomagroup.com" in calendar_list_entry["id"] or "@gmail.com" in calendar_list_entry["id"]:
                calendar_ids.append(calendar_list_entry["id"])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    print(calendar_ids)
    
    # Call the Calendar API
    mst = timezone('MST')
    print("Time in MST:", datetime.datetime.now(mst))
    appt_time_mst = datetime.datetime.now(mst)
    appt_time_iso = datetime.datetime.now(mst).isoformat() + 'Z'
    
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(datetime.datetime.utcnow())
    print("now time iso: ",datetime.datetime.utcnow().isoformat())
    
    print(appt_time_iso)
    
    date_array = (str(appt_time_mst).split())[0]
    print(date_array)
    
    start_time_mst_str = date_array + " " + "00:00:00"
    start_time_mst_strptime = datetime.datetime.strptime(start_time_mst_str, "%Y-%m-%d %H:%M:%S")
    start_mst_dt = mst.localize(start_time_mst_strptime, is_dst=None)
    start_utc_dt_str = str(start_mst_dt.astimezone(pytz.utc)).replace("+00:00", "")
    start_utc_dt_iso = datetime.datetime.strptime(start_utc_dt_str, "%Y-%m-%d %H:%M:%S").isoformat() + "Z"
    print("log", start_utc_dt_iso)
    
    
    end_time_mst_str = date_array + " " + "23:23:59"
    end_time_mst_strptime = datetime.datetime.strptime(end_time_mst_str, "%Y-%m-%d %H:%M:%S")
    end_mst_dt = mst.localize(end_time_mst_strptime, is_dst=None)
    end_utc_dt_str = str(end_mst_dt.astimezone(pytz.utc)).replace("+00:00", "")
    end_utc_dt_iso = datetime.datetime.strptime(end_utc_dt_str, "%Y-%m-%d %H:%M:%S").isoformat() + "Z"
    
    print("start utc time----> : ", start_utc_dt_iso)
    print("end utc time------> : ", end_utc_dt_iso)
    
    
    for calendar_id in calendar_ids:
        count = 0
        print('\n----%s:\n' % calendar_id)
        
        events_result = service.events().list(calendarId=calendar_id, timeMin=start_utc_dt_iso, timeMax=end_utc_dt_iso, singleEvents=True, orderBy='startTime').execute()
    
        events = events_result.get('items', [])
        
        with open('data_brandon.json', 'w') as outfile:
            json.dump(events, outfile)
        
        if not events:
            print('No upcoming events found.')
        for event in events:
            start_datetime = event['start'].get('dateTime')
            end_datetime = event['end'].get('dateTime')
            print("Event Start time-----------> : ", start_datetime)
            print("Event End time-------------> : ", end_datetime)
        # return

if __name__ == '__main__':
    main()