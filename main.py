#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, yaml
import importlib
from datetime import datetime
import json, requests

conf = yaml.load(open(sys.argv[1]).read())
data = []

for bank in conf['banks']:
    name = bank['name']
    print name
    bank['debt'] = importlib.import_module(name.lower()).get_unbilled(bank['username'], bank['password'])
    print

lines = []
for bank in conf['banks']:
    if datetime.today().day < bank['billing_cycle']:
        m = '{name}: ₹{debt[1]}'
    else:
        m = '{name}: ₹{debt[0]} | ₹{debt[1]}'
    lines.append(m.format(**bank))
message = '\n'.join(lines)

print 'Pushing notification'
headers = {
    'Access-Token': conf['pushbullet']['token'],
    'Content-Type': 'application/json'
}
data = {
    'title': 'Debt Note',
    'body': message,
    'type': 'note'
}
requests.post('https://api.pushbullet.com/v2/pushes', headers=headers, data=json.dumps(data))
