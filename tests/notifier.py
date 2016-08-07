#!/usr/bin/env python
# notifier
# A testing script to see if the email notification utility is working.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 06 21:10:51 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: notifier.py [] benjamin@bengfort.com $

"""
A testing script to see if the email notification utility is working.
"""

##########################################################################
## Imports
##########################################################################

import argparse

from datetime import datetime
from minke.utils.notify import notify
from minke.utils.humanize import HUMAN_DATETIME
from minke.utils.notify import DEFAULT_SUBJECT, DEFAULT_MESSAGE


##########################################################################
## Notifier Method
##########################################################################

def main(args):
    """
    Sends a notification email according to the params.
    """
    kwargs = {
        "subject": args.subject,
        "message": args.message,
        "fail_silent": args.fail_silent,
    }

    # send the notify - if it doesn't fail, then win!
    for recipient in args.recipient:
        notify(recipient, **kwargs)

    print("Sent {} messages".format(len(args.recipient)))


if __name__ == '__main__':

    # Command line arguments
    args = {
        ('-m', '--message'): {
            'default': DEFAULT_MESSAGE.format(datetime.now().strftime(HUMAN_DATETIME)),
            'help': 'surround message in quotes'
        },
        ('-s', '--subject'): {
            'default': DEFAULT_SUBJECT,
            'help': 'surround subject in quotes',
        },
        ('-f', '--fail-silent'): {
            'action': 'store_true',
            'default': 'false',
            'help': "don't raise an exception on failure",
        },
        ("recipient",): {
            'nargs': '+',
            'metavar': 'EMAIL',
            'help': 'recipient to send notification to',
        },
    }

    # Create the parser
    parser  = argparse.ArgumentParser()
    for pargs, kwargs in args.items():
        parser.add_argument(*pargs, **kwargs)

    # Parse the arguments and execute main
    options = parser.parse_args()
    main(options)
