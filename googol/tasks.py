from .google import *
from .gmail import *
from .drive import *


def send_email(email: str, target:str, subject: str = '', message: str = '', attach: tuple = None):
    """
    Description
    -----------
    wrapper function to create an email object and send it

    Parameters
    ----------
    subject: `str`
        subject line of the email

    message: `str`
        message being sent, the body of the email

    attach: `tuple` (OPTIONAL)
        a list of attachemtns that are to be sent

    source_email: `str`
        subject line of the email

    target_email: `str`
        message being sent, the body of the emailv
    """
    mail = GmailMessage()
    mail.build_message(subject=subject, content=message, attachments=attach)
    mail.send_email(src_email=email, dest=target)
