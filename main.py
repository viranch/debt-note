#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, yaml
import importlib
from datetime import datetime
import requests

conf = yaml.load(open(sys.argv[1]).read())
data = []

for bank in conf['banks']:
    name = bank['name']
    print name
    bank['debt'] = importlib.import_module(name.lower()).get_unbilled(bank['username'], bank['password'])
    print

lines = []
for bank in conf['banks']:
    if datetime.today().date < bank['billing_cycle']:
        m = '{name}: ₹{debt[1]} | ₹0'
    else:
        m = '{name}: ₹{debt[0]} | ₹{debt[1]}'
    lines.append(m.format(**bank))
message = '\n'.join(lines)

print 'Pushing notification'
data = {
    'app_key': conf['pushed']['key'],
    'app_secret': conf['pushed']['secret'],
    'target_type': 'app',
    'content': message
}
requests.post('https://api.pushed.co/1/push', data=data)
