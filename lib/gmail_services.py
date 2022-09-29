
from base64 import urlsafe_b64decode
from email import message
from google_services import google_service

class gmail_action(google_service):
    """docs here: https://www.thepythoncode.com/article/use-gmail-api-in-python"""
    def __init__(self, creds_file):
        app_scope = ['https://mail.google.com/']
        google_service.__init__(self, creds_file, app_scope)
        from googleapiclient.discovery import build
        self.service = build('gmail', 'v1', credentials = self.creds)


    def build_message(self, content, subject = '', attachments = {}):
        # might remove these lines below
        if subject == '':
            subject = 'no_subject'

        if len(attachments) != 0:
            attach_buf = {}

            if len(attachments) != 1:
                attach_buf[0] = attachments
            elif len(attachments) != 0:
                for i in range(len(attachments)):
                    attach_buf[i] = attachments[i]

            self.message = {'subject' : subject, 'content' : content, 'attachments' : attach_buf}

        else:
            self.message = {'subject' : subject, 'content' : content, 'attachments' : attachments}

        return self.message

    
    def build_attach(self, mail, file):
        from email.mime.text import MIMEText
        from email.mime.image import MIMEImage
        from email.mime.audio import MIMEAudio
        from email.mime.base import MIMEBase
        from mimetypes import guess_type as guess_mime_type
        import os

        os.path.abspath('file1.txt')

        content_type, encoding = guess_mime_type(file)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        try:
            if main_type == 'text':
                fp = open(file, 'rb')
                msg = MIMEText(fp.read().decode(), _subtype=sub_type)
                fp.close()
            elif main_type == 'image':
                fp = open(file, 'rb')
                msg = MIMEImage(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'audio':
                fp = open(file, 'rb')
                msg = MIMEAudio(fp.read(), _subtype=sub_type)
                fp.close()
            else:
                fp = open(file, 'rb')
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(fp.read())
                fp.close()

            file = os.path.basename(file)
            msg.add_header('Content-Disposition', 'attachment', file = file)
            mail.attach(msg)

        except FileNotFoundError:
            print("ERROR: Attachments not found. Make sure you specify full path of file you want to attach")



    def create_draft(self):
        """docs here: https://developers.google.com/gmail/api/guides/drafts"""
        print("create draft test:\n------------------------")
        print(self.message)
        # import base64
        # from email.message import EmailMessage

        # try:
        #     service = build('gmail', 'v1', credentials = self.creds)

        # except HttpError as error:
        #     print(F'An error occurred: {error}')
        #     draft = None

        # return draft
        return self.message


    def send_email(self, source_mail, target_mail):
        """docs here: https://developers.google.com/gmail/api/guides/sending"""
        print("send email test:\n------------------------------")
        print("Target Email:", target_mail)
        print("Message", self.message)
        import base64
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        if not self.message['attachments']:
            mail = MIMEText(self.message['content'])
            mail['To'] = target_mail
            mail['From'] = source_mail
            mail['Subject'] = self.message['subject']

        else:
            mail = MIMEMultipart()
            mail['To'] = target_mail
            mail['From'] = source_mail
            mail['Subject'] = self.message['subject']
            mail.attach(MIMEText(self.message['content']))

            for i in range(len(self.message['attachments'])):
                self.build_attach(mail, self.message['attachments'][i])

        self.service.users().messages().send(userId = 'me', body = {'raw': base64.urlsafe_b64encode(mail.as_bytes()).decode()}).execute()


    def add_attachments(self, attachments = ()):
        index = len(self.message['attachments'])
        for i in range(len(attachments)):
            self.message['attachments'][index + i] = attachments[i]

        return self.message





class receive_mail(gmail_action):
    """docs here: https://developers.google.com/gmail/api/guides/push"""
    def __init__(self, creds_file):
        gmail_action.__init__(self, creds_file)
