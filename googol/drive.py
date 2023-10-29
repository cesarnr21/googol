import google.auth
from .google import GoogleService
import pandas as pd
import os


class DriveAction(GoogleService):
    """
    Description
    -----------
    Tutorial here: https://www.thepythoncode.com/article/using-google-drive--api-in-python 
    Used to perform Google Drive Actions using the Google Drive API

    Parameters
    ----------
    creds_file: .json file that is downloaded from google's cloud console and is used for account verificiation

    auth_file (OPTIONAL): this pickle file used to save the verification from google and the creds_file. it help with 
        reducing the amount of times that reverifiction through a browser is done

    notify (OPTIONAL): this is used to select whether to print out output to the console
    """
    def __init__(self, notify: bool = False):
        app_scope = ['https://drive.google.com/']
        super().__init__(app_scope)
        self.notify = notify

    # should this be separate from using using folder?
    def upload_folder(self, folder_name: str, destination: str):
        pass


    def upload(self, file_name: str, destination: str):
        pass


    def create_folder(self, folder_name: str, destination: str):
        pass


    # should this be diffent from a share folder method?
    def share_file(self, file_name: str, permissions: str):
        pass


    def download_file(self, file_name: str, destination: str):
        pass


class GoogleSheet(DriveAction):
    """
    Description
    -----------
    insert description here

    Parameters
    ----------
    creds_file: .json file that is downloaded from google's cloud console and is used for account verificiation

    auth_file (OPTIONAL): this pickle file used to save the verification from google and the creds_file. it help with 
        reducing the amount of times that reverifiction through a browser is done

    notify (OPTIONAL): this is used to select whether to print out output to the console
    """
    def __init__(self, notify: bool = False):
        app_scope = 'place holder look this up'
        super().__init__(app_scope, notify)
