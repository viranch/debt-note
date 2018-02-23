#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, yaml
import hdfc, amex
import requests

conf = yaml.load(open(sys.argv[1]).read())

print 'HDFC'
hdfc_data = hdfc.get_unbilled(**conf['hdfc'])

print 'AMEX'
amex_data = amex.get_unbilled(**conf['amex'])

print 'Pushing notification'
data = {
    'app_key': conf['pushed']['key'],
    'app_secret': conf['pushed']['secret'],
    'target_type': 'app',
    'content': 'HDFC: ₹{}\nAmex: ₹{}'.format(hdfc_data, amex_data)
}
requests.post('https://api.pushed.co/1/push', data=data)
