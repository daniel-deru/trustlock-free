from datetime import timedelta, datetime, date
from os import stat
import os.path
import tzlocal
import io
import shutil
import random


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError

from utils.globals import PATH, DB_NAME, DB_COPY_NAME, DB_PATH

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/drive']


class Google:
    @staticmethod
    def connect():
        """Shows basic usage of the Google Calendar API.
            Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(f'{PATH}/integrations/google_token.json'):
            creds = Credentials.from_authorized_user_file(f'{PATH}/integrations/google_token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f'{PATH}/integrations/client_secret_dev.json', SCOPES)
                try:
                    creds = flow.run_local_server()
                except Exception:
                    return
                
            # Save the credentials for the next run
            with open(f'{PATH}/integrations/google_token.json', 'w') as token:
                token.write(creds.to_json())
    
    def save(date: date, message: str):
        print("Inside the Google save method")
        """Shows basic usage of the Google Calendar API.
            Prints the start and name of the next 10 events on the user's calendar.
    """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(f'{PATH}/integrations/google_token.json'):
            creds = Credentials.from_authorized_user_file(f'{PATH}/integrations/google_token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f'{PATH}/integrations/client_secret_dev.json', SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            with open(f'{PATH}/integrations/google_token.json', 'w') as token:
                token.write(creds.to_json())
        
        try:
            service = build('calendar', 'v3', credentials=creds, static_discovery=False)
            # Get the current datetime to convert date object to datetime for google start and end date
            current_time = datetime.now()
            
            start_date: datetime = datetime(date.year, date.month, date.day, current_time.hour, current_time.minute, current_time.second)
            end_date: datetime = start_date + timedelta(hours=1)
            timezone = str(tzlocal.get_localzone())

            event = {
                'summary': message,
                'start': {
                    'dateTime': start_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': end_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': timezone,
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                    ],
                },
            }

            event = service.events().insert(calendarId='primary', body=event).execute()
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            
    @staticmethod  
    def upload_backup():
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(f'{PATH}/integrations/google_token.json'):
            creds = Credentials.from_authorized_user_file(f'{PATH}/integrations/google_token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f'{PATH}/integrations/client_secret_dev.json', SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            with open(f'{PATH}/integrations/google_token.json', 'w') as token:
                token.write(creds.to_json())
        
        try:
            service = build("drive", "v3", credentials=creds, static_discovery=False)
                      
            files = []
            page_token = None
            while True:
                response = service.files().list(q="mimeType='application/octet-stream'").execute()
                files.extend(response.get('files', []))
                page_token = response.get("nextPageToken", None)
                if page_token == None: break
            

            file_id: str or None = None
            file_exists: bool = False
            for file in files:
                if "name" in file and file['name'] == DB_NAME:
                    file_id = file['id']
                    file_exists = True
                    break
            
            if file_exists:
                service.files().delete(fileId=file_id).execute()

            file_metadata = {'name': DB_NAME}
            media = MediaFileUpload(f'{PATH}/database/{DB_NAME}', mimetype='application/octet-stream')
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            
        except HttpError as error:
            print('An error occurred: %s' % error)
    
    @staticmethod      
    def download_backup():
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        print("inside the google download method")
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(f'{PATH}/integrations/google_token.json'):
            creds = Credentials.from_authorized_user_file(f'{PATH}/integrations/google_token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f'{PATH}/integrations/client_secret_dev.json', SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            with open(f'{PATH}/integrations/google_token.json', 'w') as token:
                token.write(creds.to_json())
        
        try:
            service = build("drive", "v3", credentials=creds, static_discovery=False)
            
            files = []
            page_token = None
            while True:
                response = service.files().list(q="mimeType='application/octet-stream'").execute()
                files.extend(response.get('files', []))
                page_token = response.get("nextPageToken", None)
                if page_token == None: break
                
                
            file_id: str or None = None    
            for file in files:
                if "name" in file and file['name'] == DB_NAME:
                    file_id = file['id']
            file = None
            try:
                file = service.files().get_media(fileId=file_id)
            except Exception:
                return None
            
            download = io.BytesIO()
            downloader = MediaIoBaseDownload(download, file)
            done = False
            
            while not done:
                status, done = downloader.next_chunk()
            
            download.seek(0)

            # Copy data to a copy of the database
            with open(f"{DB_PATH}{DB_COPY_NAME}", "wb") as f:
                shutil.copyfileobj(download, f)
            
            return DB_COPY_NAME
            
        except HttpError as error:
            print('An error occurred: %s' % error)





