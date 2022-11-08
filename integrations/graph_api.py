import webbrowser
import os
import sys
import re
import pyperclip
import json
import time
from typing import Match
from msal import PublicClientApplication

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils.globals import PATH

from utils.message import Message


class Microsoft():
    _APPLICATION_ID: str = '8bcf81ba-398d-4e2c-a23e-823c517d6681'
    _AUTHORITY_URL: str = "https://login.microsoftonline.com/consumers/"
    _SCOPES: list[str] = ["Files.ReadWrite", "Files.Read", "Files.Read.All", "Files.ReadWrite.All"]
    _GRAPH_API_ENDPOINT: str = "https://graph.microsoft.com/v1.0/"
    TOKEN_FILE: str = f"{PATH}/integrations/microsoft_tokens.json"
    
    def __init__(self):
        # Create an instance of a public client application
        self.app: PublicClientApplication = PublicClientApplication(
            self._APPLICATION_ID,
            authority=self._AUTHORITY_URL
        )
        
        # Only request this once
        self.access_token = self.get_access_token()

    
    def create_token_file(self, tokens: object) -> None:
        token_json = json.dumps(tokens)
        
        with open(self.TOKEN_FILE, "w") as token_file:
            token_file.write(token_json)
            
    def authenticate_app(self) -> object:

        
        # Start the device flow
        try:
            self.flow = self.app.initiate_device_flow(scopes=self._SCOPES)
        except Exception as error:
            with open(f"{PATH}/error.txt", "a") as error_file:
                error_file.write(f"\n\n{error}")
        
        
        # Get the code that the user needs to authenticate the app and copy the code
        self.code: None or Match[str] = re.search(r"(?<=code )[A-Z0-9]{1,20}", self.flow['message'])
        
        Message(
            f"You will be asked to enter the following code: {self.code.group()}. The code is already copied to your clipboard.", 
            "Enter Authentication Code"
        ).exec_()
        
        pyperclip.copy(self.code.group())
        
        # Open a webbrowser to authenticate the app
        webbrowser.open_new_tab(self.flow['verification_uri'])
        
        # Get the access and refresh tokens to use the Graph API
        tokens: object = self.app.acquire_token_by_device_flow(self.flow)
        
        # Create the custom token object
        tokens_dict: object = self.create_token_object(tokens=tokens)
        
        # Create the token file
        self.create_token_file(tokens=tokens_dict)
        
        return tokens_dict
    
    def get_access_token(self) -> str:
        # Boolean to check if the token file exists 
        token_file_exists: bool = os.path.exists(self.TOKEN_FILE)
        
        # Initialize variable to hold tokens
        tokens: None or object
        
        # if the file doesn't exist authenticate the app to create the tokens and token file
        if not token_file_exists:
            tokens = self.authenticate_app()
        else:
           
            # Open the token file and get the tokens
            with open(self.TOKEN_FILE, "r") as token_file:
                token_json = token_file.read()
                tokens = json.loads(token_json)
                
            current_time: float = time.time()
            
            # if the access token has expired generate a new access token with the refresh token
            if int(tokens['access_token_expiry']) <=  current_time:
                
                tokens = self.generate_new_tokens(tokens)
                
        return tokens["access_token"]
            
                
    def generate_new_tokens(self, tokens: object):
        current_time: float = time.time()
        new_tokens: None or object
        
        # If the refresh token expired authenticate the app to get new tokens
        if int(tokens['refresh_token_expiry']) <= current_time:
            
            new_tokens = self.authenticate_app()
        else:
            
            # get the new tokens from the access token and save them in the token file
            response = self.app.acquire_token_by_refresh_token(tokens['refresh_token'], scopes=self._SCOPES)
            print(response)
            new_tokens = self.create_token_object(response)
            self.create_token_file(new_tokens)
            
        return new_tokens
            
    def create_token_object(self, tokens: object) -> object:
        
        # Get the current Unix timestamp in seconds
        current_time = time.time()
        
        if tokens == None: 
            print("The tokens don't exist")
            return
        
        # Time in seconds that the access token is valid since the time of request
        access_token_duration = int(tokens['expires_in'])
        
        # The refresh token is valid for 90 days from the time of request according to Microsoft
        _89_days = 60*60*24*89
        
        tokens_dict = {
            "access_token": tokens["access_token"],
            "refresh_token": tokens['refresh_token'],
            "access_token_expiry": current_time + access_token_duration,
            "refresh_token_expiry": current_time + _89_days
        } 
        
        return tokens_dict