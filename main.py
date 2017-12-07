#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random
from my_config_parser import MyConfigParser
from mailer import Mailer

def match_mail_recipients(recipients):
    new_list = {}
    mixed_list = recipients.copy()
    original_list = recipients.copy()
    
    while len(mixed_list) > 0:
        if len(recipients) > 0:
            recipient = random.choice(list(recipients.keys()))
        else:
            break
        while True:
            partner = random.choice(list(mixed_list.keys()))
            if original_list[recipient] != original_list[partner]:
                break
            elif len(mixed_list) <= 1:
                mixed_list = original_list.copy()
                recipients = original_list.copy()
            
        new_list[recipient] = original_list[recipient]
        new_list[recipient]['partner'] = original_list[partner]['name']
        mixed_list.pop(partner)
        recipients.pop(recipient)
        
    return new_list

def print_usage():
    print(sys.argv[0], "matches mail partners.")
    print("Usage:", sys.argv[0], "<config-file>")
    print("See config folder for a sample config file")

if (__name__ == '__main__'):
    
    if len(sys.argv) == 2:
        config_path = sys.argv[1]
    else:
        print_usage()
        exit(1)
    
    try:
        config = MyConfigParser(config_path)
    except ValueError as val_err:
        print('Maleformed config file.', file=sys.stderr)
        print(val_err, file=sys.stderr)
        exit(1)

    mailer = Mailer(config['SMTP'])
    mailer.connect()
    maildata = config['Mail']
    partner_list = match_mail_recipients(config['Recipients'])
    for recipient in partner_list:
        maildata['to'] = partner_list[recipient]['mail']
        maildata['message'] = maildata['template'].replace(maildata['mark'], partner_list[recipient]['partner'])
        mailer.sendmail(maildata)
    mailer.disconnect()
    exit(0)
