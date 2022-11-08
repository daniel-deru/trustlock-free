import requests
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from integrations.graph_api import Microsoft
from utils.globals import PATH, DB_NAME, DB_PATH, DB_COPY_NAME

class OneDrive(Microsoft):
    
    def __init__(self):
        super(OneDrive, self).__init__()
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        
    def upload(self, file=f"{DB_PATH}{DB_NAME}") -> None:
        # Endpoint to upload the file
        endpoint = self._GRAPH_API_ENDPOINT + f"/me/drive/items/root:/{os.path.basename(file)}:/content"
        
        # Initialize variable to hold the binary byte strings of the file
        data: None or bytes
        
        # Read the data in the file to the data variable
        with open(file, "rb") as upload:
            data = upload.read()
        
        # Make a PUT request to upload the file
        request: requests.Response = requests.put(endpoint, headers=self.headers, data=data)
        # Get the response
        response = request.json()

        # Return the file id to the onedrive worker to save in the database
        return response['id']

    def download(self, file_id):
        # file_id = "2EFAE4DC031AAE4E!18648"
        endpoint = self._GRAPH_API_ENDPOINT + f"/me/drive/items/{file_id}/content"
        
        response_file: requests.Response = requests.get(endpoint, headers=self.headers)
        
        if response_file.status_code == 200:
            with open(f"{DB_PATH}{DB_COPY_NAME}", "wb") as file:
                file.write(response_file.content)
            
            return DB_COPY_NAME
        else:
            if response_file.status_code == 404:
                return None
            print("response file get request failed")
            print(response_file.status_code)
            return None
            
    def get_file_name(self, file_id) -> str:
 
        file_name_request = requests.get(
            self._GRAPH_API_ENDPOINT + f"/me/drive/items/{file_id}",
            headers=self.headers,
            params={'select': 'name'}
        )
        file_name = file_name_request.json().get('name')
        
        return file_name
            
           
# onedrive = OneDrive()
# onedrive.upload()
# onedrive.download()
        
        
    