import requests
from datetime import date

def get_unbilled(username, password):
    client_id, secret, account_token = password.split(',')

    print('Reading balances')
    data = requests.post('https://development.plaid.com/accounts/balance/get', json={
        'client_id': client_id,
        'secret': secret,
        'access_token': account_token
    }, headers={'Content-Type': 'application/json'}).json()

    if 'error_code' in data:
        raise Exception(data['error_code'])

    cards = {a['mask']: a['balances']['current'] for a in data.get('accounts', []) if a['subtype'] == 'credit card'}
    current = sum(cards.values())

    print(current)
    return (str(0), str(current))

def get_category_spending(username, password, budget_config):
    client_id, secret, account_token = password.split(',')

    bucket_totals = {}

    print('Reading transactions')
    today = date.today()
    start_date = date(today.year, today.month, 1).strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')
    data = requests.post('https://development.plaid.com/transactions/get', json={
        'client_id': client_id,
        'secret': secret,
        'access_token': account_token,
        'start_date': start_date,
        'end_date': end_date,
        'options': {'count': 500}
    }, headers={'Content-Type': 'application/json'}).json()

    #print(data)
    for trx in data['transactions']:
        trx_cat = trx['category'][-1]
        trx_desc = trx['name']
        for bucket in budget_config['buckets']:
            lbl = bucket['label']
            categories = [lbl] + bucket.get('categories', [])
            if (trx_cat in categories or any(desc in trx_desc for desc in bucket.get('descriptions', []))) and not any(desc in trx_desc for desc in bucket.get('exclude_descriptions', [])):
                bucket_totals.setdefault(lbl, []).append({'amount': trx['amount'], 'desc': trx['name']})
    print(bucket_totals)

    bucket_totals = dict((k, sum(t['amount'] for t in v)) for k, v in bucket_totals.items())

    return bucket_totals
