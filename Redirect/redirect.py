REDIRECT_TARGET_HOST = 'xxxxx.cloudfront.net'


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
