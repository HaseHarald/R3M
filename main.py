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

try:
    config = MyConfigParser("config/testconfig.yml")
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
    maildata['message'] = partner_list[recipient]['name'] + " matches " + partner_list[recipient]['partner']
    mailer.sendmail(maildata)
mailer.disconnect()
exit(0)
