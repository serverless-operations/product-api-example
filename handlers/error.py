import json
import base64
import gzip
import requests


def handler(event, context):
    decoded_data = base64.b64decode(event['awslogs']['data'])
    json_data = json.loads(gzip.decompress(decoded_data))
    print(json_data)
    requests.post(
        url='https://hooks.slack.com/services/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',
        headers={
            'Content-Type': 'application/json'
        },
        data=json.dumps({'text': json_data['logEvents'][0]['message']})
    )