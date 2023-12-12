"""tests the functionality of the GoogolEmail Parent Class"""

import unittest
from googol import GoogolEmail
from email.mime.multipart import MIMEMultipart
from testdata import DATA_PATH, TEST_FILES


class NominalCase(unittest.TestCase):
    def test_email(self):
        self.email = GoogolEmail()
        self.email.build_message(subject = 'test/test_send_email',
                            content = 'content of email',
                            attachments = (TEST_FILES['album'], TEST_FILES['textfile']),
            )

        # FIXME: add assert here


    def test_attachements(self):
        new_attachments = ('file3', 'file4')
        self.email.add_attachments(new_attachments)

        # FIXME: add assert here for attachement count

        mail = MIMEMultipart()

        for attachement in self.email.message['attachments']:
            self.email.build_attach(mail, attachement)

            # FIXME: add assert here
