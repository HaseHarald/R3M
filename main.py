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

mailer = Mailer(config)
mailer.connect()
mailer.sendmail()
mailer.disconnect()
exit(0)
