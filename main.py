#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
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
    bank_module = importlib.import_module(name.lower())
    bank['debt'] = bank_module.get_unbilled(bank['username'], bank['password'])
    bank['cat_spend'] = bank_module.get_category_spending(bank['username'], bank['password'], conf['budget_tracker'])
    print

lines = []
currency_totals = {}
budget_spends = {}
for bank in banks:
    debt = bank['debt']
    totals = currency_totals.setdefault(bank['currency'], [0, 0])
    if datetime.today().day < bank['billing_cycle'] + 5:
        m = '{name}: {currency}{debt[0]} | {currency}{debt[1]}'
        totals[0] += float(debt[0].replace(',', ''))
        totals[1] += float(debt[1].replace(',', ''))
    else:
        m = '{name}: {currency}{debt[1]}'
        totals[0] += float(debt[1].replace(',', ''))
    lines.append(m.format(**bank))

    cat_spend = bank['cat_spend']
    for label, amount in cat_spend.iteritems():
        budget_spends[label] = budget_spends.get(label, 0) + amount

for totals in currency_totals.values():
    if totals[1] == 0:
        totals.pop()
if len(currency_totals) > 1 or len(banks) > 1:
    lines.extend('Total: ' + ' | '.join('{}{}'.format(cur, t) for t in tot) for cur, tot in currency_totals.iteritems())

if len(budget_spends) > 0:
    lines.append('\nBudgets:')
    for label, amount in sorted(budget_spends.items(), key=lambda i: i[1], reverse=True):
        lines.append('${} {}'.format(amount, label))

message = '\n'.join(lines)

if os.getenv('DEBUG', False):
    print message
else:
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
