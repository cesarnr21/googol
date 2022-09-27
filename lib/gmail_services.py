
from google_services import google_service

class gmail_action(google_service):
    """docs here: https://www.thepythoncode.com/article/use-gmail-api-in-python"""
    def __init__(self, creds_file):
        app_scope = ['https://mail.google.com/']
        google_service.__init__(self, creds_file, app_scope)
        from googleapiclient.discovery import build
        build('gmail', 'v1', credentials = self.creds)


    def build_message(self, content, subject = '', attachments = ''):
        # might remove these lines below
        if subject == '':
            subject = 'no_subject'

        message = {'subject' : subject, 'content' : content, 'attachments' : attachments}
        return message


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
        return message


    def send_email(self, target_email, message):
        """docs here: https://developers.google.com/gmail/api/guides/sending"""
        print("send email test:\n------------------------------")
        print("Target Email:", target_email)
        print("Message", message)
        import base64
        from email.message import EmailMessage

        from email.mime.text import MIMEText


        email = EmailMessage()

        email.set_content(message['content'])

        email['To'] = target_email
        email['From'] = 'source_email'
        email['Subject'] = message['subject']

        place_hold = False
        if place_hold:
            from email.mime.multipart import MIMEMultipart
            from email.mime.image import MIMEImage
            from email.mime.audio import MIMEAudio
            from email.mime.base import MIMEBase
            from mimetypes import guess_type as guess_mime_type


        # pass


    def add_attachemnts(self, message, attachments):
        for i in range(len(attachments)):
            message['attachments'][i] = attachments[i]

            """working theory for already having attachments"""
            """
            index = len(message['attachments']) # get the lenght of the current attachments
            message['attachments'][index] = attachments[i]
            """

        return message


    def find_email(self):
        pass





class receive_mail():
    """docs here: https://developers.google.com/gmail/api/guides/push"""
    def __init__(self):
        pass
