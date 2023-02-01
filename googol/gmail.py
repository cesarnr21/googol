from base64 import urlsafe_b64decode
from email import message
from typing import Dict
from .google import GoogleService
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type
import os
from pathlib import Path


class GmailMessage(GoogleService):
    """
    Description
    -----------
    docs here: https://www.thepythoncode.com/article/use-gmail-api-in-python

    Used to build and send emails using the Gmail API

    Parameters
    ----------
    creds_file: `str`
        json file that is downloaded from google's cloud console and is used for account verificiation

    auth_file: `str` (OPTIONAL)
        this pickle file used to save the verification from google and the creds_file. it help with 
        reducing the amount of times that reverifiction through a browser is done

    notify: `bool` (OPTIONAL)
        this is used to select whether to print out output to the console

    Methods
    -------
    `__init__(creds_file: str, auth_file: str, notify: bool)`: 
        initializes the object

    `build_message(subject: str, content: str, attachments: tuple)`:
        This is used to put together the message being sent.

    `add_attachments(new_attachmnets: tuple)`:
        used to add attachments to the object

    `send_email(source_email: str, destination_email: str)`:
        this method sends out the email object
    """
    def __init__(self, creds_file: str, auth_file: str = None, notify: bool = False):
        app_scope = ['https://mail.google.com/']
        super().__init__(app_scope, creds_file, auth_file)
        from googleapiclient.discovery import build
        self.service = build('gmail', 'v1', credentials = self.creds)
        self.notify = notify


    def build_message(self, subject: str = '', content: str = '', attachments: tuple = ''):
        """
        Description
        -----------
        This is used to put together the message being sent.

        Parameters
        ----------
        subject: `str`
            subject line of the email

        contents: `str`
            message being sent, the body of the email

        attachments: `tuple` (OPTIONAL)
            a list of attachemtns that are to be sent

        Return
        ------
        contents: includes all of the content from the file. This is due to the fact later in the script,
            writing the file removes all of the content of the file, so it has to be rewritten

        headers: a list that includes all the headers in format [index, header_rank, header_string]

        placement: stores the line where the table of contents will be inserted
        """
        if subject == '':
            subject = 'no_subject'

        if len(attachments) != 0:
            attach_buf = []

            if len(attachments) == 1:
                attach_buf[0] = attachments
            else:
                for i in range(len(attachments)):
                    attach_buf.append(attachments[i])

            self.message = {'subject': subject, 'content': content, 'attachments': attach_buf}

        else:
            self.message = {'subject': subject, 'content': content, 'attachments': attachments}

        return self.message


    def build_attach(self, mail, attachment) -> None:
        """
        looks for attachments and encodes them, gets them ready to be sent
        """
        content_type, encoding = guess_mime_type(attachment)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'

        main_type, sub_type = content_type.split('/', 1)

        try:
            if main_type == 'text':
                with open(attachment, 'rb') as file:
                   msg = MIMEText(file.read().decode(), _subtype = sub_type)

            elif main_type == 'image':
                with open(attachment, 'rb') as file:
                   msg = MIMEImage(file.read(), _subtype = sub_type)

            elif main_type == 'audio':
                with open(attachment, 'rb') as file:
                    msg = MIMEAudio(file.read(), _subtype = sub_type)

            else:
                with open(attachment, 'rb') as file:
                    msg = MIMEBase(main_type, sub_type)
                msg.set_payload(file.read())

            attachment = os.path.basename(attachment)
            msg.add_header('Content-Disposition', 'attachment', file = attachment)
            mail.attach(msg)

        except FileNotFoundError:
            print(attachment)
            print("ERROR: Attachments not found. Make sure you specify full path of file you want to attach")


    def create_draft(self):
        """
        docs here: https://developers.google.com/gmail/api/guides/drafts
        will most likely not use this function
        """
        print("create draft test:\n------------------------")
        print(self.message)
        return self.message


    def send_email(self, source_mail: str, target_mail: str | tuple | list) -> None:
        """
        Description
        -----------
        This is used to put together the message being sent.
        docs here: https://developers.google.com/gmail/api/guides/sending

        Parameters
        ----------
        source_email: `str`
            subject line of the email

        target_email: `str`
            message being sent, the body of the email

        Return
        ------
        No returns
        """
        if isinstance(target_mail, str):
            recipients = 1
        elif isinstance(target_mail, list) or isinstance(target_mail, tuple):
            recipients = len(target_mail)

        for i in range(recipients):
            if not self.message['attachments']:
                mail = MIMEText(self.message['content'])
                mail['To'] = target_mail if isinstance(target_mail, str) else target_mail[i]
                mail['From'] = source_mail
                mail['Subject'] = self.message['subject']

            else:
                mail = MIMEMultipart()
                mail['To'] = target_mail if isinstance(target_mail, str) else target_mail[i]
                mail['From'] = source_mail
                mail['Subject'] = self.message['subject']
                mail.attach(MIMEText(self.message['content']))

                for i in range(len(self.message['attachments'])):
                    self.build_attach(mail, self.message['attachments'][i])

            self.service.users().messages().send(userId = 'me', body = {'raw': base64.urlsafe_b64encode(mail.as_bytes()).decode()}).execute()


    def add_attachments(self, attachments: tuple = ()):
        """
        Description
        -----------
        Used to add attachemnts to the email object
        docs here: https://developers.google.com/gmail/api/guides/sending

        Parameters
        ----------
        attachments: `tuple`
            a list of attachemtns that are to be sent
        """
        for i in range(len(attachments)):
            self.message['attachments'].append(attachments[i])

        return self.message


class GmailAction(GoogleService):
    """docs here: 
    https://developers.google.com/gmail/api/guides/push 
    https://www.thepythoncode.com/article/use-gmail-api-in-python#Reading_Emails
    """

    def __init__(self, creds_file: str = None, auth_file: str = None, notify: bool = False):
        app_scope = ['https://mail.google.com/']
        super().__init__(app_scope, creds_file, auth_file)
        from googleapiclient.discovery import build
        self.service = build('gmail', 'v1', credentials = self.creds)
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
