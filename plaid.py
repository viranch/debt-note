import requests

def get_unbilled(username, password):
    client_id, secret, account_token = password.split(',')
    print 'Reading data'
    data = requests.post('https://development.plaid.com/accounts/balance/get', json={
        'client_id': client_id,
        'secret': secret,
        'access_token': account_token
    }, headers={'Content-Type': 'application/json'}).json()

    cards = {a['mask']: a['balances']['current'] for a in data.get('accounts', []) if a['subtype'] == 'credit card'}
    current = sum(cards.values())

    return (str(0), str(current))
