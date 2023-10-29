from base64 import urlsafe_b64decode
from email import message
from typing import Sequence
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from pathlib import Path

from .google import GoogleService
from .email import GoogolEmail


class GmailMessage(GoogleService, GoogolEmail):
    """Used to build and send emails using the Gmail API

    docs here: https://www.thepythoncode.com/article/use-gmail-api-in-python

    Parameters
    ----------
    credentials_file: `str | Path` (OPTIONAL)
        json file that is downloaded from google's cloud console and is used for account verificiation

    notify: `bool` (OPTIONAL)
        this is used to select whether to print out output to the console
    """
    def __init__(self, credentials_file: str | Path = None, notify: bool = False):
        app_scope = ['https://mail.google.com/']
        super().__init__(app_scope, credentials_file)
        from googleapiclient.discovery import build
        self.service = build('gmail', 'v1', credentials = self.credentials)
        self.notify = notify


    def send_email(self, src_email: str, dest: Sequence) -> None:
        """Send Email
        docs here: https://developers.google.com/gmail/api/guides/sending

        Parameters
        ----------
        src_email: `str`
            Email of sender

        dest: `str`
            Email of recipient
        """
        recipients = 1 if isinstance(dest, str) else len(dest)

        # TODO: add email/phone verifier, if dest is a phone number, then lookup network email

        for index in range(recipients):
            mail = MIMEMultipart()
            mail['To'] = dest if isinstance(dest, str) else dest[index]
            mail['From'] = src_email
            mail['Subject'] = self.message['subject']
            mail.attach(MIMEText(self.message['content']))

            if not isinstance(self.message['attachments'], type(None)):
                for attachment in self.message['attachments']:
                    self.build_attach(mail, attachment)

            # FIXME: redownload
            self.service.users().messages().send(userId = 'me', body = {'raw': base64.urlsafe_b64encode(mail.as_bytes()).decode()}).execute()



class GmailAction(GoogleService):
    """docs here: 
    https://developers.google.com/gmail/api/guides/push 
    https://www.thepythoncode.com/article/use-gmail-api-in-python#Reading_Emails
    """

    def __init__(self,notify: bool = False):
        app_scope = ['https://mail.google.com/']
        super().__init__(app_scope)
        from googleapiclient.discovery import build
        self.service = build('gmail', 'v1', credentials = self.credentials)
        self.notify = notify


    def get_size_format(self, b, factor = 1024, suffix="B"):
        """
        Scale bytes to its proper byte format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if b < factor:
                return f"{b:.2f}{unit}{suffix}"
            b /= factor
        return f"{b:.2f}Y{suffix}"


    def clean(self, text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)


    def search_email(self, query):
        result = self.service.users().messages().list(userId = 'me', q = query).execute()
        self.messages = [ ]
        if 'messages' in result:
            self.messages.extend(result['messages'])

        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = self.service.users().messages().list(userId = 'me', q = self.query, pageToken = page_token).execute()

            if 'messages' in result:
                self.messages.extend(result['messages'])

        # find a better way to fix this
        if len(self.messages) == 0:
            self.messages = 'no emails found'

        return self.messages


    def print_messages(self):
        print("Found", len(self.messages), "that matched the search query")
        for msg in self.messages:
            self.read_message(msg)


    def parse_parts(self, parts, folder_name, message):
        """Utility function that parses the content of an email partition"""
        if parts:
            for part in parts:
                filename = part.get("filename")
                mimeType = part.get("mimeType")
                body = part.get("body")
                data = body.get("data")
                file_size = body.get("size")
                part_headers = part.get("headers")

                if part.get("parts"):
                    self.parse_parts(self.service, part.get("parts"), folder_name, message)

                if mimeType == "text/plain":
                    if data:
                        text = urlsafe_b64decode(data).decode()
                        print(text)

                elif mimeType == "text/html":
                    if not filename:
                        filename = "index.html"

                    filepath = os.path.join(folder_name, filename)
                    print("Saving HTML to", filepath)
                    with open(filepath, "wb") as file:
                        file.write(urlsafe_b64decode(data))

                else:
                    # attachment other than a plain text or HTML
                    for part_header in part_headers:
                        part_header_name = part_header.get("name")
                        part_header_value = part_header.get("value")
                        if part_header_name == "Content-Disposition":
                            if "attachment" in part_header_value:
                                # we get the attachment ID 
                                # and make another request to get the attachment itself
                                print("Saving the file:", filename, "size:", self.get_size_format(file_size))
                                attachment_id = body.get("attachmentId")
                                attachment = self.service.users().messages().attachments().get(id = attachment_id, userId = 'me', messageId = message['id']).execute()
                                data = attachment.get("data")
                                filepath = os.path.join(folder_name, filename)
                                if data:
                                    with open(filepath, "wb") as file:
                                        file.write(urlsafe_b64decode(data))


    def read_message(self, message: list, non_attach: tuple = None) -> None:
        self.message = {}
        msg = self.service.users().messages().get(userId = 'me', id = message['id'], format = 'full').execute()
        payload = msg['payload']
        headers = payload.get('headers')
        parts = payload.get('parts')
        self.attachments = payload.get('parts')
        #self.parse_parts(parts, message) # might not even need this

        if parts:
            for part in parts:
                file_name = part.get("filename")
                mimeType = part.get("mimeType")
                body = part.get("body")
                data = body.get("data")
                file_size = body.get("size")
                part_headers = part.get("headers")

                if file_name not in non_attach:

                    if part.get("parts"):
                        self.parse_parts(self.service, part.get("parts"), message)

                    if mimeType == "text/plain":
                        if data:
                            self.message['text'] = urlsafe_b64decode(data).decode()

                    elif mimeType == "text/html":
                        self.message['html'] = urlsafe_b64decode(data)

                    else:
                        for part_header in part_headers:
                            part_header_name = part_header.get("name")
                            part_header_value = part_header.get("value")
                            if part_header_name == "Content-Disposition":
                                if "attachment" in part_header_value:
                                    # we get the attachment ID 
                                    # and make another request to get the attachment itself
                                    print("Saving the file:", file_name, "size:", self.get_size_format(file_size))

                                    # put this somewhere below:
                                    index = len(self.message['attachments'])
                                    self.message['attachments'][index]['id'] = body.get("attachmentId")

                                    attachment_id = body.get("attachmentId")


    def print_email(self): # complete this
        print("=" * 50)


    def save_email(self, folder, file_name: str) -> None: # make this way better
        if not file_name:
            file_name = "index.html"

        filepath = os.path.join(folder, file_name)
        print("Saving HTML to", filepath)
        with open(filepath, "wb") as f:
            f.write(self.message['html'])


    # needs to be fixed
    def save_attachments(self, folder: str) -> None:
        file_name = ''
        if not os.path.isdir(folder):
            os.mkdir(folder)

        attachment_id = self.message['attachments']
        file_size = 'place_holder'

        attachment = self.service.users().messages().attachments().get(id = attachment_id, userId = 'me', messageId = message['id']).execute()

        data = attachment.get("data")
        file_path = os.path.join(file_name)
        if data:
            with open(file_path, "wb") as file:
                file.write(urlsafe_b64decode(data))

            print("Saving the file:", file_name, "size:", self.get_size_format(file_size))


    def mark_as_read(self):
        messages_to_mark = self.search_email()
        # remove after done
        print("Matched emails:", len(messages_to_mark))
        return self.service.users().messages().batchModify(userId = 'me', body = {'ids': [msg['id'] for msg in messages_to_mark], 'removeLabelIds': ['UNREAD']}).execute()


    def mark_as_unread(self):
        messages_to_mark = self.search_email()
        # remove after done
        print("Matched emails:", len(messages_to_mark))
        return self.service.users().messages().batchModify(userId = 'me', body = {'ids': [msg['id'] for msg in messages_to_mark], 'addLabelIds': ['UNREAD']}).execute()


    def delete_email(self):
        messages_to_delete = self.search_email()
        return self.service.users().messages().batchDelete(userId = 'me', body = {'ids': [msg['id'] for msg in messages_to_delete]}).execute()


def create_query(*query: str) -> tuple[str]:
    """create a query to seach email. operators list from: https://support.google.com/mail/answer/7190 """
    query = query
    return query
