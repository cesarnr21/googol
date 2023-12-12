import google.auth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pathlib import Path
import pickle
import os

AUTHORIZATION_FILE = 'GOOGLE_CREDENTIALS_FILE'
PICKLE_CREDENTIALS_FILE = 'GOOGLE_CREDENTIALS_PICKLE_FILE'


class GoogleService():
    """Parent class for the individual classes for some google services, 
    used to reduce/eliminate the re-verification process for all classes

    docs here: https://www.thepythoncode.com/article/use-gmail-api-in-python 

    FIXME: fixe spelling/grammar below
    when the class is initialized, if an `auth_file.pickle` is not give/does not exits, then
    it create one to store the info from Google's verification 

    Parameters
    ----------
    app_scope: `list[str]`
        used to determine what actions the API has access to.
    """
    def __init__(self, app_scope: list[str], credentials_file: Path = None) -> None:
        self.app_scope = app_scope

        try:
            if isinstance(credentials_file, type(None)):
                self.credentails_file = Path(os.environ[PICKLE_CREDENTIALS_FILE])
                authorization_file = Path(os.environ[AUTHORIZATION_FILE])
            else:
                self.authorization = credentials_file
        # FIXME: what if the enviroment variable doesn't exists, 
        # add stuff to deal with it
        except KeyError:
            print(f'Create an enviroment variable to load')

        if self.credentails_file.exists():
            with open(self.credentails_file, 'rb') as token:
                self.credentials = pickle.load(token)

            self._verify_pickle(authorization_file=self.credentails_file)

        elif authorization_file.exists():
            self._store_pickle(authorization_file=authorization_file)

        # FIXME: what if the files don't exist
        else:
            print('add function here to do stuff')
            pass


    def _store_pickle(self, authorization_file: Path) -> None:
        flow = InstalledAppFlow.from_client_secrets_file(authorization_file, self.app_scope)
        self.credentials = flow.run_local_server(port = 0)

        with open(self.credentails_file, 'wb') as token:
            pickle.dump(self.credentials, token)


    def _verify_pickle(self, authorization_file: Path) -> None:
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(authorization_file, self.app_scope)
                self.credentials = flow.run_local_server(port = 0)

            with open(self.credentails_file, 'wb') as token:
                pickle.dump(self.credentials, token)
