import google.auth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pathlib import Path
import pickle


class GoogleService():
    """
    Description
    -----------
    docs here: https://www.thepythoncode.com/article/use-gmail-api-in-python 
    parent class for the individual classes for various Google Service
    Used to reduce/eliminate the re-verification process for all classes

    when the class is initialized, if an `auth_file.pickle` is not give/does not exits, then
    it create one to store the info from Google's verification 

    Methods
    -------
    `__init__(app_scope: list[str], creds_file: str = None, auth_file: str = None) -> None`
        initializes the object

    Parameters
    ----------
    app_scope: `list[str]`
        used to determine what actions the API has access to.

    creds_file: `str`
        json file that is downloaded from google's cloud console and is used for account verificiation

    auth_file: `str` (OPTIONAL)
        this pickle file used to save the verification from google and the creds_file. it help with 
        reducing the amount of times that reverifiction through a browser is done
    """
    def __init__(self, app_scope: list[str], creds_file: str = None, auth_file: str = None) -> None:
        self.creds = None
        if Path.exists(auth_file):
            with open(auth_file, 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())

            else:  
                flow = InstalledAppFlow.from_client_secrets_file(creds_file, app_scope)
                self.creds = flow.run_local_server(port = 0)

            with open(auth_file, 'wb') as token:
                pickle.dump(self.creds, token)
