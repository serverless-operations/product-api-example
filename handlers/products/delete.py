"""商品削除API."""
import os
import boto3
from lib.utils import response_builder
from lib.decorators import api_handler
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


@api_handler
def handler(event, context):
    """商品削除API."""
    try:
        # URLパスから更新対象の商品IDを取得
        product_id = event.get('pathParameters').get('productId')

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

        # 自分自身がownerのデータがチェック（他人のデータは消せない）
        if (product.get('Item').get('Value') != event.get('requestContext').get('authorizer').get('jwt').get('claims').get('name')):
            return response_builder(404, {
                'error_message': 'request data is not found'
            })

        # 削除対象のデータを取得
        result = products_table.query(
            KeyConditionExpression=Key('Id').eq(product_id)
        )

        # 対象データの削除
        for item in result.get('Items'):
            products_table.delete_item(Key={
                'Id': product_id,
                'Key': item.get('Key')
            })

        return response_builder(204, {})
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return response_builder(404, {
                'error_message': 'request data is not found'
            })
        raise e
    except Exception as e:
        raise e
