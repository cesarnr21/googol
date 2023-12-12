"""tests the functionality of the gmail object"""

import unittest
import os
from googol import GmailMessage, GmailAction
from testdata import DATA_PATH, TEST_FILES
from datetime import datetime


class NominalCase(unittest.TestCase):
    def test_send_email(self):
        email = GmailMessage()
        current = datetime.now()

        email.build_message(subject = 'test/test_send_email',
                            content = f'Googol GMAIL Test on {current:%B %d, %Y at %I:%M %p}',
                            attachments = TEST_FILES['textfile'],
            )

        email.send_email(src_email=os.environ['TEST_SRC_EMAIL'],
                         dest=os.environ['TEST_EMAIL'])

        print('done')


    def test_read_email(self):
        pass


if __name__ == '__main__':
    unittest.main()

