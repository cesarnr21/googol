# Notes on Google APIs

<br>

## Set Up API
To use Google Services and APIs, they need to be setup
> Reference: <https://www.thepythoncode.com/article/use-gmail-api-in-python>

<br>

Install the necessary dependencies

```bash
$ python3 -m install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

1. Enable API for Services that you want to access. Get a Token from **[Google's API Dashboard](https://console.cloud.google.com/apis/dashboard?pli=1&project=ceres-server)**. It might be necessary to create a Cloud Project to be able to enable APIs

2. Once the project is created, select **`ENABLE APIS AND SERVICES`** then search for the API you want enable, for example the **Gmail API**

3. Enable the API and then on the left of screen go to **`Credentials`** and **`CREATE CREDENTIALS`**

4. Select **`OAuth client ID`** from the options and fill out the requested info **Web application -> [choose client-name] -> Save**. Download the Client ID as a json file

5. In the left side of the screen, select **`OAuth consent screen`** and make sure that the publishing status is set to `Testing`

6. Create an enviroment variable **`GOOGLE_CREDENTIALS_FILE`** to store the path location of the Client ID json file

7. Also, create a **`GOOGLE_CREDENTIALS_PICKLE_FILE`** enviroment variable to save a `pickle` token to minimize the amount of authentication needed.

<br>
<br>

## Gmail Search Query
For a full list of Gmail search Operators, go here: <https://support.google.com/mail/answer/7190>

--------------------------------------------------------

| **Operator** | **Use** | **Example** |
|---|---|---|
| `from:` | Specify the sender | `from:email@address.com` |
| `to:` | Specify the recipient | `to:email@address.com` |
| `cc:` | Recipient of carbon copy | `cc:email@address.com` |
| `bcc:` | Recipient of blind carbon copy | `bcc:email@address.com` |
| `subject:` | Words in subject line | `subject:subject line` |
| `has:` | Emails that have attachements, Google Drive,<br>Docs, Sheets, Slides, YouTube Video, or Link | `has:attachment`<br>`has:drive`<br>`has:presentation`<br>`has:spreadsheet`<br>`has:document`<br>`has:youtube` |
| `filename:` | Attachments with a certain name or file type | `filename:pdf`<br>`filename:file1.txt` |
| `" "` | Use double qoutes for an exact search | `"text"` |
| `label:` | Messages that have a certain label | `label:important`<br>`label:inbox` |
| `in:` | To search in a specific folder | `in:inbox`<br>`in:trash`<br>`in:spam` |
| `is:` | Messages that are marked as: important, read,<br>unread, starred, snoozed. | `is:important`<br>`is:read`<br>`is:unread`<br>`is:starred`<br>`is:snoozed` |
| `after:` | Messages received/sent after a certain date | `after:2004/04/16`<br>or<br>`after:04/16/2004` |
| `before:` | Messages received/sent before a certain date | `before:2004/04/16`<br>or<br>`before:04/16/2004` |
| `older_than:`<br>and <br>`newer_than:` | Search for messages older or newer than a <br>time period using d(days), m(months), y(years) | `older_than:2d`<br>`newer_than:1d` |


