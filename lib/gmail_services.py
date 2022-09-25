
from google_services import google_service

class gmail_action(google_service):
    def __init__(self):
        google_service.__init__(self)


    def create_draft(self, message):
        """docs here: https://developers.google.com/gmail/api/guides/drafts"""
        print("create draft test:\n------------------------")
        print(message)
        # import base64
        # from email.message import EmailMessage

        # try:
        #     service = build('gmail', 'v1', credentials = self.creds)

        # except HttpError as error:
        #     print(F'An error occurred: {error}')
        #     draft = None

        # return draft


    def send_email(self, target_email, message):
        """docs here: https://developers.google.com/gmail/api/guides/sending"""
        print("send email test:\n------------------------------")
        print("Target Email:", target_email)
        print("Message", message)
        # import base64
        # from email.message import EmailMessage

        # import google.auth
        # from googleapiclient.discovery import build
        # from googleapiclient.errors import HttpError


        # creds, _ = google.auth.default()

        # try:
        #     service = build('gmail', 'v1', credentials = creds)

        #     email = EmailMessage()

        #     email.set_content(message['content'])

        #     email['To'] = target_email
        #     email['From'] = 'source_email'
        #     email['Subject'] = message['subject']

        # except HttpError as error:
        #     print(F'An error occurred: {error}')
        #     draft = None


        # pass


    def add_attachemnt(self, message, attachments):
        message['attachments'] = attachments
        return message


    def find_email(self):
        pass





class receive_mail():
    """docs here: https://developers.google.com/gmail/api/guides/push"""
    def __init__(self):
        pass
