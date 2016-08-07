# minke.utils.notify
# Helper functions to send notification emails via Gmail.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 06 17:05:40 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: notify.py [3d75c52] benjamin@bengfort.com $

"""
Helper functions to send notification emails via Gmail.
"""

##########################################################################
## Imports
##########################################################################

import os
import smtplib

from email import encoders
from datetime import datetime
from email.utils import formatdate
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from minke.config import settings
from minke.exceptions import NotifyError
from minke.utils.humanize import HUMAN_DATETIME


##########################################################################
## Message Constants
##########################################################################

DEFAULT_SUBJECT = "CloudScope Notification"
DEFAULT_MESSAGE = "A notification was triggered on {}"

##########################################################################
## Email Notifications
##########################################################################

def notify(recipient, subject=None, message=None, **kwargs):
    """
    Notifies the recipient at the given email address by sending an email
    with the subject and message in it. Meant to be used sparingly.
    """

    # Get the default subject and message
    subject = subject or DEFAULT_SUBJECT
    message = message or DEFAULT_MESSAGE.format(
        datetime.now().strftime(HUMAN_DATETIME)
    )

    # Get the arguments from the settings
    sender   = kwargs.get('sender', settings.notify.username)
    username = kwargs.get('username', settings.notify.username)
    password = kwargs.get('password', settings.notify.password)
    host     = kwargs.get('host', settings.notify.email_host)
    port     = kwargs.get('port', settings.notify.email_port)
    mimetype = kwargs.get('mimetype', 'plain')
    fail_silent = kwargs.get('fail_silent', settings.notify.fail_silent)

    # Create the email message
    msg = MIMEMultipart()
    msg['From']= sender
    msg['To'] = recipient
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    # Attach the mime text to the message
    msg.attach(MIMEText(message, mimetype))

    # Attach any files to the email
    for fpath in kwargs.get('files', []):
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(fpath, 'rb').read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition', 'attachment; filename={}'.format(
                os.path.basename(fpath)
            )
        )
        msg.attach(part)

    # Attempt to send the message
    try:

        # Do the smtp thing
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login(username, password)
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()

        # Return message success
        return True

    except Exception as e:
        if not fail_silent:
            raise NotifyError(str(e))

        # Return message failure
        return False
