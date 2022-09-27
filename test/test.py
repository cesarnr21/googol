# template for creating messages and using a messanges

import json

project_path = __file__[:-len('test/test.py')]

settings = project_path + 'test.json'

with open(settings, 'r') as file:
    config = json.load(file)

import sys
sys.path.append(project_path + './lib')
from gmail_services import gmail_action

from datetime import datetime
now = datetime.now()

email = gmail_action(creds_file = config['ceres_gapi_creds'])
message = email.build_message(subject = 'Initial Test', content = 'Current time is ' + now.strftime('%H:%M:%S'))

# email.create_draft(message)
email.add_attachments(message, attachments = ('file1.txt', 'file542.txt', 'screenshot.png'))
email.send_email(config['target_email'], message)
