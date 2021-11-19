"""商品一覧取得API."""
import os
import json
import boto3
import base64
import datetime
from lib.utils import response_builder
from lib.decorators import api_handler
from boto3.dynamodb.conditions import Key


@api_handler
def handler(event, context):
    """商品一覧取得API."""
    try:
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=os.getenv('DynamoDBEndpoint')
        )
        products_table = dynamodb.Table(os.getenv('ProductsTableName'))

        # リクエストにnextToken(ページング)がある場合はDynamoDBに渡せるように展開
        query = event.get('queryStringParameters') or {}
        if query.get('nextToken') is not None:
            # 登録日の降順で対象データを取得(ページング)
            items = products_table.query(
                IndexName='SearchIndex',
                KeyConditionExpression=Key('Key').eq('registrationDt'),
                Limit=5,
                ScanIndexForward=False,
                ExclusiveStartKey=json.loads(base64.b64decode(query.get('nextToken').encode('utf-8')).decode('utf-8'))
            )
        else:
            # 登録日の降順で対象データを取得
            items = products_table.query(
                IndexName='SearchIndex',
                KeyConditionExpression=Key('Key').eq('registrationDt'),
                Limit=5,
                ScanIndexForward=False
            )

        # レスポンスデータの商品情報配列を生成
        response_body_products = []
        for item in items.get('Items'):
            product = products_table.get_item(Key={
                'Id': item.get('Id'),
                'Key': 'info'
            })
            response_body_products.append({
                'id': item.get('Id'),
                'name': product.get('Item').get('Name'),
                'imageUrl': product.get('Item').get('ImageUrl'),
                'price': product.get('Item').get('Price'),
                'description': product.get('Item').get('Description'),
                'registrationDt': datetime.datetime.fromtimestamp(int(item.get('Value'))).isoformat()
            })

        # レスポンスデータのBody本体を生成
        response_body = {
            'count': items.get('Count'),
            'products': response_body_products
        }

        # ページングが存在する場合はその情報をレスポンスに追加
        if items.get('LastEvaluatedKey') is not None:
            nextToken = base64.b64encode(json.dumps(items.get('LastEvaluatedKey')).encode('utf-8'))
            response_body |= {
                'nextToken': nextToken.decode('utf-8')
            }

        return response_builder(200, response_body)
    except Exception as e:
        raise e
