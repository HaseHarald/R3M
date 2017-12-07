# -*- coding: utf-8 -*-

import sys
import smtplib

# TODO: A hack of a lot more exceptionhandling!

class Mailer:
    def __init__(self, config):
        self.config = config
    
    def connect(self):
        self.server = smtplib.SMTP(self.config['SMTP']['server'], self.config['SMTP']['port'])
        self.server.ehlo()
        if self.config['SMTP']['starttls']:
            self.server.starttls()
        self.server.ehlo()
        try:
            self.server.login(self.config['SMTP']['user'], self.config['SMTP']['password'])
        except smtplib.SMTPAuthenticationError as auth_error:
            print("SMTP Authentication Error", file=sys.stderr)
            print(auth_error, file=sys.stderr)
            self.disconnect()
            exit(1)
        
    def sendmail(self):
        message = 'From: ' + self.config['Mail']['from'] + '\nSubject: ' + self.config['Mail']['subject'] + '\n\n' + self.config['Mail']['message']
        try:
            self.server.sendmail(self.config['Mail']['from'], self.config['Mail']['to'], message)
        except smtplib.SMTPServerDisconnected:
            print("No connection to SMTP server", file=sys.stderr)
            exit(2)
        
    def disconnect(self):
        self.server.rset()
        self.server.quit()
