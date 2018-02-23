#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, yaml
import importlib
import requests

conf = yaml.load(open(sys.argv[1]).read())
data = []

for bank in conf['banks']:
    name = bank.pop('name')
    print name
    debt = importlib.import_module(name.lower()).get_unbilled(**bank)
    data.append({'name': name, 'debt': debt})
    print

print 'Pushing notification'
data = {
    'app_key': conf['pushed']['key'],
    'app_secret': conf['pushed']['secret'],
    'target_type': 'app',
    'content': '\n'.join('{name}: ₹{debt}'.format(**d) for d in data)
}
requests.post('https://api.pushed.co/1/push', data=data)
