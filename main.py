#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from my_config_parser import MyConfigParser
from mailer import Mailer

try:
    config = MyConfigParser("config/testconfig.yml")
except ValueError as val_err:
    print('Maleformed config file.', file=sys.stderr)
    print(val_err, file=sys.stderr)
    exit(1)

mailer = Mailer(config['SMTP'])
mailer.connect()
maildata = config['Mail']
for recipient in config['Recipients']:
    maildata['to'] = config['Recipients'][recipient]['mail']
    mailer.sendmail(maildata)
mailer.disconnect()
exit(0)
