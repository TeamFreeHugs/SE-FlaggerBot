import requests
# from globalvars import GlobalVars


def accept(fkey):
    response = requests.post('https://stackexchange.com/oauth/dialog', data={
        'client_id': 5583,
        'scope': 'write_access',
        'redirect_uri': 'https://stackexchange.com/oauth/login_success',
        'response_type': 'token',
        'state': '',
        'fkey': fkey,
        'user_action': 'Approve'
    })
    return response
