# -*- coding: utf-8 -*-

import sys
import smtplib
from unidecode import unidecode

# TODO: A hack of a lot more exceptionhandling!

class Mailer:
    def __init__(self, config):
        self.config = config
    
    def connect(self):
        self.server = smtplib.SMTP(self.config['server'], self.config['port'])
        self.server.ehlo()
        if self.config['starttls']:
            self.server.starttls()
        self.server.ehlo()
        try:
            self.server.login(self.config['user'], self.config['password'])
        except smtplib.SMTPAuthenticationError as auth_error:
            print("SMTP Authentication Error", file=sys.stderr)
            print(auth_error, file=sys.stderr)
            self.disconnect()
            exit(1)
        
    def sendmail(self, maildata):
        message = 'From: ' + maildata['from'] + '\nSubject: ' + maildata['subject'] + '\n\n' + maildata['message']
        try:
            self.server.sendmail(maildata['from'], maildata['to'], unidecode(message))
        except smtplib.SMTPServerDisconnected:
            print("No connection to SMTP server", file=sys.stderr)
            exit(2)
        
    def disconnect(self):
        self.server.rset()
        self.server.quit()
