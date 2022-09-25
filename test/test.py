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

message = {'Initial Test': 'Current time is ' + now.strftime('%H:%M:%S')}
email = gmail_action()
email.create_draft(message)
email.send_email(config['target_email'], message)
