#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from my_config_parser import MyConfigParser

try:
    config = MyConfigParser("config/testconfig.yml")
except ValueError as val_err:
    print('Maleformed config file. Main', file=sys.stderr)
    print(val_err, file=sys.stderr)
    exit(1)

print("Config:", config)
exit(0)
