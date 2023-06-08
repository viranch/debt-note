#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys, yaml
import importlib
from datetime import datetime
import requests

conf = yaml.safe_load(open(sys.argv[1]).read())
data = []

# optionally filter by name for debugging
banks = [b for b in conf['banks'] if len(sys.argv) < 3 or b['name'].lower() == sys.argv[2].lower()]

nbanks = []

for bank in banks:
    name = bank['name']
    print(name)
    bank['currency'] = bank['currency'].strip() #.encode('utf-8').strip()
    bank_module = importlib.import_module(name.lower())
    try:
        bank['debt'] = bank_module.get_unbilled(bank['username'], bank['password'])
        bank['ndebt'] = tuple(round(float(d.replace(',', '')), 2) for d in bank['debt'])
        if sum(bank['ndebt']) != 0:
            nbanks.append(bank)
            bank['cat_spend'] = bank_module.get_category_spending(bank['username'], bank['password'], conf['budget_tracker'])
    except Exception as e:
        bank['error'] = e
    print()

lines = []
currency_totals = {}
budget_spends = {}
for bank in banks:
    err = bank.get('error')
    if err is not None:
        lines.append(f'{bank["name"]}: {err}')
        continue

    debt, ndebt = bank['debt'], bank['ndebt']
    if sum(ndebt) == 0:
        continue

    totals = currency_totals.setdefault(bank['currency'], [0, 0])
    if datetime.today().day < bank['billing_cycle'] + 5:
        m = '{name}: {currency}{debt[0]} | {currency}{debt[1]}'
        totals[0] += ndebt[0]
        totals[1] += ndebt[1]
    else:
        m = '{name}: {currency}{debt[1]}'
        totals[0] += ndebt[1]
    lines.append(m.format(**bank))

    cat_spend = bank.get('cat_spend', {})
    for label, amount in cat_spend.items():
        budget_spends[label] = budget_spends.get(label, 0) + amount

for totals in currency_totals.values():
    if totals[1] == 0:
        totals.pop()
if len(currency_totals) > 1 or len(nbanks) > 1:
    lines = ['Total: ' + ' | '.join(f'{cur}{round(t, 2)}' for t in tot) for cur, tot in currency_totals.items()] + lines

if len(budget_spends) > 0:
    lines.append('\nBudgets:')
    for label, amount in sorted(budget_spends.items(), key=lambda i: i[1], reverse=True):
        lines.append(f'${round(amount, 2)} {label}')

message = '\n'.join(lines)

if os.getenv('DEBUG', False):
    print(message)
else:
    print('Pushing notification')
    pb = conf.get('pushbullet')
    po = conf.get('pushover')
    if pb:
        headers = {
            'Access-Token': pb['token'],
            'Content-Type': 'application/json'
        }
        data = {
            'title': 'Debt Note',
            'body': message,
            'type': 'note'
        }
        requests.post('https://api.pushbullet.com/v2/pushes', headers=headers, json=data)
    if po:
        requests.post('https://api.pushover.net/1/messages.json', data={
            'user': po['user_key'],
            'token': po['api_key'],
            'message': message,
        })
