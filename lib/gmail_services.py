import google.auth
from google_services import google_service

class gmail_action(google_service):
    def __init__(self):
        google_service.__init__(self)
        print("this is a gmail service")

