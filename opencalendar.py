import datetime, json, pytz
import pickle
import os.path
import httplib2
from pytz import timezone
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Calendar:

    # SCOPES = ['https://www.googleapis.com/auth/calendar']
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    # SCOPES = ['https://www.googleapis.com/auth/calendar']



    def calendar(self, appt_time_obj, appt_timezone_str):
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
                    'credentials.json', self.SCOPES)
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
        # appt_time_obj
        # appt_timezone_str = 
        
        # mst = timezone('MST')
        # print(mst)
        # print("Time in MST:", datetime.datetime.now(mst))
        # appt_time_mst = datetime.datetime.now(mst)
        # appt_time_iso = datetime.datetime.now(mst).isoformat() + 'Z'
        
        # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        # print(datetime.datetime.utcnow())
        # print("now time iso: ", datetime.datetime.utcnow().isoformat())
        
        # print(appt_time_iso)
        
        
        
        if "PST" in appt_timezone_str:
            appt_timezone = timezone('US/Pacific')
        elif "MST" in appt_timezone_str:
            appt_timezone = timezone('MST')
            
            
        appt_time = appt_time_obj.astimezone(appt_timezone)
        appt_timestamp = datetime.datetime.timestamp(appt_time)
        
        print(appt_time, appt_timestamp)
               
        
        date_array = (str(appt_time_obj).split())[0]
        print(date_array)
        
        start_time_mst_str = date_array + " " + "00:00:00"
        start_time_mst_strptime = datetime.datetime.strptime(start_time_mst_str, "%Y-%m-%d %H:%M:%S")
        start_mst_dt = appt_timezone.localize(start_time_mst_strptime, is_dst=None)
        start_utc_dt_str = str(start_mst_dt.astimezone(pytz.utc)).replace("+00:00", "")
        start_utc_dt_iso = datetime.datetime.strptime(start_utc_dt_str, "%Y-%m-%d %H:%M:%S").isoformat() + "Z"
        print("log", start_utc_dt_iso)
        
        
        end_time_mst_str = date_array + " " + "23:23:59"
        end_time_mst_strptime = datetime.datetime.strptime(end_time_mst_str, "%Y-%m-%d %H:%M:%S")
        end_mst_dt = appt_timezone.localize(end_time_mst_strptime, is_dst=None)
        end_utc_dt_str = str(end_mst_dt.astimezone(pytz.utc)).replace("+00:00", "")
        end_utc_dt_iso = datetime.datetime.strptime(end_utc_dt_str, "%Y-%m-%d %H:%M:%S").isoformat() + "Z"
        
        print("start utc time----> : ", start_utc_dt_iso)
        print("end utc time------> : ", end_utc_dt_iso)
        
        agent_info = {
            "name" : "",
            "email" : ""
        }
        
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
                
                agent_val = self.available_agent(appt_time, start_datetime, end_datetime)
                
                if agent_val == "Busy":
                    break
            
            print(calendar_id, agent_val)
            if agent_val == "Available":
                # if "eugene" in calendar_id:
                #     agent_name = "Eugene Quackenbush"
                if "penneymullins" in calendar_id:
                    agent_name = "Penney Mullins"
                elif "brandon" in calendar_id:
                    agent_name = "Brandon LaVallee"
                elif "frank" in calendar_id:
                    agent_name = "Frank Vazquez"
                
                agent_info["name"] = agent_name
                agent_info["email"] = calendar_id
                
                return agent_info

        return agent_info
    
    def available_agent(self, appt_time, start_datetime, end_datetime):
        
        appt_timestamp = datetime.datetime.timestamp(appt_time)
        
        start_calendartime_str = start_datetime
        start_calendartime = datetime.datetime.fromisoformat(start_calendartime_str)
        start_calendar_timestamp = datetime.datetime.timestamp(start_calendartime)
        
        
        end_calendartime_str = end_datetime
        end_calendartime = datetime.datetime.fromisoformat(end_calendartime_str)
        end_calendar_timestamp = datetime.datetime.timestamp(end_calendartime)
        
        
        print("Appt Timestamp--------------> ", int(appt_timestamp))
        print("Start Calendar Timestamp----> ", int(start_calendar_timestamp))
        print("End Calendar Timestamp------> ", int(end_calendar_timestamp))
        
        if int(appt_timestamp) > int(start_calendar_timestamp) and int(appt_timestamp) < int(end_calendar_timestamp):
            print("***********************************************")
            agent_avl = "Busy"
        else:
            agent_avl = "Available"
        
        print(agent_avl)
        
        return agent_avl