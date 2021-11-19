"""商品更新API."""
import os
import boto3
import jsonschema
from lib.utils import response_builder
from lib.decorators import api_handler
from botocore.exceptions import ClientError
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
    """商品更新API."""
    try:
        # URLパスから更新対象の商品IDを取得
        product_id = event.get('pathParameters').get('productId')

        # リクエストBodyを取得
        body = event.get('body')

        # リクエストデータのバリデーション
        jsonschema.validate(body, json_schema)

        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=os.getenv('DynamoDBEndpoint')
        )
        products_table = dynamodb.Table(os.getenv('ProductsTableName'))

        # 更新対象の存在チェック
        product = products_table.get_item(Key={
            'Id': product_id,
            'Key': 'owner'
        })

        # 自分自身がownerのデータがチェック
        if (product.get('Item').get('Value') != event.get('requestContext').get('authorizer').get('jwt').get('claims').get('name')):
            return response_builder(404, {
                'error_message': 'request data is not found'
            })

        # データの更新
        products_table.put_item(
          Item={
              'Id': product_id,
              'Key': 'info',
              'Name': body.get('name'),
              'ImageUrl': body.get('imageUrl'),
              'Price': body.get('price'),
              'Description': body.get('description')
          }
        )

        return response_builder(204, {})
    except jsonschema.ValidationError as e:
        return response_builder(400, {
            'error_message': e.message
        })
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return response_builder(404, {
                'error_message': 'request data is not found'
            })
        raise e
    except Exception as e:
        raise e
