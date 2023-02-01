# searching for emails

import sys, os
from googol import GmailAction
from googol import create_query
from pathlib import Path


project_path = Path(__file__).parent.parent
data_path = project_path / 'data/'

creds = Path('path/google_creds.json')
token = Path('path/token.pickle')

email = GmailAction(creds_file=creds, auth_file=token, notify=True)
query = create_query('test 3', 'to:ceres.assistant@gmail.com')
email.search_email(query)

non_attach = ('tmobilespace.gif', 'dottedline600.gof', 'footer.gif')

#email.read_message(email.messages[0], non_attach)
email.read_message(email.messages)
email.print_messages()
email.mark_as_unread()      # marks emails as unread
email.mark_as_read()        # marks emails as read
email.delete_email()        # deletes emails
