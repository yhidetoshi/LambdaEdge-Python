"""
- 許可IPアドレス元の場合は認証なし
- 許可されたIPアドレス以外の場合はBasic認証を実施
"""

import base64

ALLOW_USERS = [
    {
        "user": "admin",
        "password": "pass1"
    }, {
        "user": "dev",
        "password": "pass2"
    }
]

ALLOW_IP = ['X.X.X.X', 'X.X.X.X']

ERROR_RESPONSE_AUTH = {
    'status': '401',
    'statusDescription': 'Unauthorized',
    'body': 'Authentication Failed',
    'headers': {
            'www-authenticate': [
                {
                    'key': 'WWW-Authenticate',
                    'value': 'Basic Authentication'
                }
            ]
    }
}


def lambda_handler(event, context):
    request = event['Records'][0]['cf']['request']
    headers = request['headers']
    client_ip = event['Records'][0]['cf']['request']['clientIp']

    if validate_client_ip(client_ip):
        return request

    # Authorizationヘッダーの有無をチェック
    if 'authorization' not in headers:
        return ERROR_RESPONSE_AUTH

    encode_auth = headers['authorization'][0]['value'].split(" ")
    decode_auth = base64.b64decode(encode_auth[1]).decode().split(":")
    (user, password) = (decode_auth[0], decode_auth[1])

    if validate_auth(user, password):
        return request
    else:
        return ERROR_RESPONSE_AUTH


def validate_auth(user, password):
    exist_flag = False
    for allow_user in ALLOW_USERS:
        if user == allow_user.get('user') and password == allow_user.get('password'):
            exist_flag = True
            return True

    if exist_flag == False:
        return False


def validate_client_ip(client_ip):
    print('CLIENT_IP=%s' % client_ip)
    if client_ip in ALLOW_IP:
        return True
    else:
        return False
