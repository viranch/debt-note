import json
import requests
import datetime

def get_unbilled(username, password):
    print 'Logging in'
    session = requests.Session()
    headers = {'content-type': 'application/json'}

    auth = {'email': username, 'password': password}
    r = session.post('https://bb2.creditstacks.com/user', headers=headers, data=json.dumps(auth))
    headers['authorization'] = r.json()['accessToken']

    print 'Reading data'
    q = {'query': '{me{transactions {transactionTime,type,amount,status} }}'}
    r = session.get('https://bb2.creditstacks.com/api-v1', headers=headers, data=json.dumps(q))
    data = r.json()['data']['me']['transactions']

    print 'Logging out'
    session.delete('https://bb2.creditstacks.com/user', headers=headers)
    session.close()

    today = datetime.date.today()
    this_month = today.strftime('%Y%m')
    last_month = (today.replace(day=1) - datetime.timedelta(days=1)).strftime('%Y%m')
    balances = [0, 0]
    for trx in data:
        if trx['status'] not in ['SETTLED', 'PENDING']:
            continue
        dt = datetime.datetime.strptime(' '.join(trx['transactionTime'].split()[1:4]), '%b %d %Y').strftime('%Y%m')
        if dt == last_month:
            bal_idx = 0
        elif dt == this_month:
            bal_idx = 1
        else:
            continue
        if trx['type'] == 'TXN':
            balances[bal_idx] += trx['amount']
        elif trx['type'] == 'RETURN':
            balances[bal_idx] -= trx['amount']

    return (str(balances[0]), str(balances[1]))
