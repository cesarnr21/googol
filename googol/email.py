from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type
from typing import Sequence
import os
from pathlib import Path


class GoogolEmail:
    """FIXME: add appropiate docstring here

    Created a separte class to allow these methods to be used with classes that don't use
    the gmail service

    Also should help to separately unit test this code
    """

    def build_message(self, subject: str = None, content: str = None, attachments: Sequence = None) -> dict:
        """Put together the message being sent.

        Parameters
        ----------
        subject: `str` (OPTIONAL)
            subject line of the email

        contents: `str` (OPTIONAL)
            message being sent, the body of the email

        attachments: `Sequence` (OPTIONAL)
            a Sequence of attachemtns that are to be sent

        Return
        ------
        message: a `dict` object with an email subject, content, attachements
        """
        self.message = {'subject': subject, 'content': content, 'attachments': {attachments}}

        return self.message


    def build_attach(self, mail, attachment) -> None:
        """FIXME: add an appropiate docstring

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
        """FIXME: add an appropiate docstring

        docs here: https://developers.google.com/gmail/api/guides/drafts
        will most likely not use this function
        """
        print("create draft test:\n------------------------")
        print(self.message)
        return self.message


    def add_attachments(self, attachments: tuple = ()):
        """FIXME: add an appropiate docstring
        """
        for i in range(len(attachments)):
            self.message['attachments'].append(attachments[i])

        return self.message
