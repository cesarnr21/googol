# Google Services
Just some modules that allow to use some Google Services. Install using:
`make install` or `python3 -m pip install --editable .`

To use Google Services and APIs, they need to be setup in the developer board. **[Instructions here](/docs/using.md#set-up-api)**

Then download the API credentials to a `json` file and create an enviroment variable `GOOGLE_CREDENTIALS_FILE` that points to its path. Also, create a `GOOGLE_CREDENTIALS_PICKLE_FILE` enviroment variable to minimize the amount of authentication needed.

<<<<<<< HEAD
> Note that this package is only meant for personal use, use at your own risk.
=======
>>>>>>> 8af9540 (add task)

## Gmail Module
### Sending Emails
The `gmail.py` module includes the class `GmailMessage` which allows to send emails and attachments. To send an email:
1. Used the `build_message(subject: str, content: str, attachments: Union[str, tuple])` function. This is used to put together the message being sent.
    - Another way to add attachements to the email message is to use the `add_attachments()` function. Argument can either be a `string` for a single attachment or a `tuple` for multiple. It is important to add the full path of the attachment. The `os.path.anspath()` can be used to help with this.
2. `send_email()` can be used after building a message to send the email. The arguments are the source email and a destination email address.
```py
from googol import GmailMessage

subject = 'email subject'
content = 'content of email'
attachments = ('file1', 'file2')

email = GmailMessage(creds_file, auth_file)
email.build_message(subject, content, attachments)

new_attachments = ('file3', 'file4')
email.add_attachments(new_attachments)
email.send_email('source email', 'destination email')
```

### Reading Emails
To read emails, use the `GmailAction` class. 

More specify query options here: [Google APIs Notes](docs/google_APIs.md#Gmail-Query)
### Other Actions

## Google Drive and Google Sheets
The `google_drive.py` module includes the class `DriveAction` which will have the capability to upload 

