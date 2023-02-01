"""
This is a script to test the capability of creating and sending an email with attachments
"""

from datetime import datetime
from googol import GmailMessage
from pathlib import Path


project_path = Path(__file__).parent.parent
data_path = project_path / 'data/'

creds = Path('path/google_creds.json')
token = Path('path/token.pickle')

now = datetime.now()

subject = 'Test on ' + now.strftime('%A %B %d, %Y at %-I:%M %p')
content = 'Files: '
attachments = (data_path / 'file1.txt', data_path / 'google-products.jpg')

email = GmailMessage(creds_file = creds, auth_file = token)
email.build_message(subject, content)

# new_attachments = (data_path / 'file542.txt', data_path / 'screenshot.png')
# email.add_attachments(new_attachments)
email.send_email('ceres.assistant@gmail.com', '2674695888@tmomail.net')
