#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, yaml
import importlib
from datetime import datetime
import json, requests

conf = yaml.load(open(sys.argv[1]).read())
data = []

# optionally filter by name for debugging
banks = [b for b in conf['banks'] if len(sys.argv) < 3 or b['name'].lower() == sys.argv[2].lower()]

for bank in banks:
    name = bank['name']
    print name
    bank['currency'] = bank['currency'].encode('utf-8').strip()
    bank['debt'] = importlib.import_module(name.lower()).get_unbilled(bank['username'], bank['password'])
    print

lines = []
currency_totals = {}
for bank in banks:
    debt = bank['debt']
    totals = currency_totals.setdefault(bank['currency'], [0, 0])
    if datetime.today().day < bank['billing_cycle']:
        m = '{name}: {currency}{debt[1]}'
        totals[0] += float(debt[1].replace(',', ''))
    else:
        m = '{name}: {currency}{debt[0]} | {currency}{debt[1]}'
        totals[0] += float(debt[0].replace(',', ''))
        totals[1] += float(debt[1].replace(',', ''))
    lines.append(m.format(**bank))

for totals in currency_totals.values():
    if totals[1] == 0:
        totals.pop()
lines.extend('Total: ' + ' | '.join('{}{}'.format(cur, t) for t in tot) for cur, tot in currency_totals.iteritems())
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
