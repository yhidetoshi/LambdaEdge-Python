import re

### すべてのリクエストを別ホストにリダイレクトする ###
REDIRECT_TARGET_HOST = 'fuga.cloudfront.net'


def lambda_handler(event, context):
    redirect_response = {
        'status': '301',
        'statusDescription': 'Moved Permanently',
        'headers': {
            'location': [
                {
                    'key': 'Location',
                    'value': f'http://{REDIRECT_TARGET_HOST}'
                }
            ]
        }
    }
    return redirect_response


### 特定のパス配下のアクセスを同じホストの別パスにリダイレクトする ###
# /v1/ --> /v2/
# - hoge.cloudfront.net/v1/index.html --> hoge.cloudfront.net/v2/index.html
"""
PATH_PATTERN = '^\/v1\/'


def lambda_handler(event, context):
    request = event['Records'][0]['cf']['request']
    headers = request['headers']

    host = headers['host'][0]['value']
    uri = request['uri']

    if (re.match(PATH_PATTERN, uri)):
        redirect_response = {
            'status': '301',
            'statusDescription': 'Moved Permanently',
            'headers': {
                'location': [
                    {
                        'key': 'Location',
                        'value': f'http://{host}/v2/index.html'
                    }
                ]
            }
        }
        return redirect_response
    return request
"""

### 特定のパス配下のアクセスを別ホストにリダイレクトする ###
# - hoge.cloudfront.net/index.html --> hoge.cloudfront.net/index.html
# - hoge.cloudfront.net/v1/index.html --> fuga.cloudfront.net/v1/index.html
#     - uri="/v2/index.html"
# - hoge.cloudfront.net/v2/index.html --> fuga.cloudfront.net/v2/index.html
#     - uri="/v1/index.html"

"""
PATH_PATTERN = '^\/v1\/|^\/v2\/'
REDIRECT_TARGET_HOST = 'fuga.cloudfront.net'


def lambda_handler(event, context):
    request = event['Records'][0]['cf']['request']
    uri = request['uri']

    if (re.match(PATH_PATTERN, uri)):
        redirect_response = {
            'status': '301',
            'statusDescription': 'Moved Permanently',
            'headers': {
                'location': [
                    {
                        'key': 'Location',
                        'value': f'http://{REDIRECT_TARGET_HOST}{uri}'
                    }
                ]
            }
        }
        return redirect_response
    return request
"""


### ホスト名指定の場合はリダイレクトしない。pathは引き継ぐ ###
# - hoge.cloudfront.net --> hoge.cloudfront.net
# - hoge.cloudfront.net/index.html --> fuga.cloudfront.net/index.html

"""
REDIRECT_TARGET_HOST = 'fuga.cloudfront.net'

def lambda_handler(event, context):
    request = event['Records'][0]['cf']['request']
    headers = request['headers']

    if headers['host'][0]['value'] == REDIRECT_TARGET_HOST:
        return request

    uri = request['uri']

    redirect_response = {
        'status': '301',
        'statusDescription': 'Moved Permanently',
        'headers': {
            'location': [
                {
                    'key': 'Location',
                    'value': f'http://{REDIRECT_TARGET_HOST}{uri}'
                }
            ]
        }
    }

    return redirect_response
"""
