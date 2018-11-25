import json
import requests

def get_unbilled(username, password):
    print 'Logging in'
    session = requests.Session()
    headers = {'content-type': 'application/json'}

    auth = {'email': username, 'password': password}
    r = session.post('https://bb2.creditstacks.com/user', headers=headers, data=json.dumps(auth))
    headers['authorization'] = r.json()['accessToken']

    print 'Reading data'
    q = {'query': '{me{account{coreData{openToBuy,creditLimit}}}}'}
    r = session.get('https://bb2.creditstacks.com/api-v1', headers=headers, data=json.dumps(q))
    data = r.json()['data']['me']['account']['coreData']

    print 'Logging out'
    session.delete('https://bb2.creditstacks.com/user', headers=headers)
    session.close()

    balance = data['creditLimit'] - data['openToBuy']

    return (None, str(balance))
