"""新規商品追加API."""
import os
import boto3
import uuid
import time
import jsonschema
from lib.utils import response_builder
from lib.decorators import api_handler

json_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'imageUrl': {'type': 'string'},
        'price': {'type': 'string'},
        'description': {'type': 'string'}
    },
    'required': [
        'name',
        'imageUrl',
        'price',
        'description'
    ]
}


@api_handler
def handler(event, context):
    """新規商品追加API."""
    try:
        # リクエストBodyを取得
        body = event.get('body')

        # リクエストデータのバリデーション
        jsonschema.validate(body, json_schema)

        # 商品IDを生成
        id = str(uuid.uuid4())

        # 商品データの登録処理
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=os.getenv('DynamoDBEndpoint')
        )
        products_table = dynamodb.Table(os.getenv('ProductsTableName'))
        products_table.put_item(
          Item={
              'Id': id,
              'Key': 'info',
              'Name': body.get('name'),
              'ImageUrl': body.get('imageUrl'),
              'Price': body.get('price'),
              'Description': body.get('description')
          }
        )

        products_table.put_item(
          Item={
              'Id': id,
              'Key': 'registrationDt',
              'Value': str(int(time.time()))
          }
        )
        products_table.put_item(
          Item={
              'Id': id,
              'Key': 'owner',
              'Value': event.get('requestContext').get('authorizer').get('jwt').get('claims').get('name')
          }
        )

        # 商品の登録に成功してHTTPステータス201と商品IDをレスポンス
        return response_builder(203, {
            'product_id': id
        })
    except jsonschema.ValidationError as e:
        return response_builder(400, {
            'error_message': e.message
        })
    except Exception as e:
        raise e
