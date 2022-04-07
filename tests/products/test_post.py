"""新規商品追加のユニットテスト."""
import os
import boto3
from handlers.products import post
from lib.utils import parse_body


class TestPostProducts(object):
    """新規商品追加のユニットテスト."""

    def test_validation_body_missing_name(self, missing_name_data):
        """Bodyのパラメータにnameが存在しない場合は400エラーを返す."""
        result = post.handler(missing_name_data, {})
        assert result.get('statusCode') == 400
        assert result.get('body') == '{"error_message": "\'name\' is a required property"}'

    def test_validation_body_missing_image_url(self, missing_image_url_data):
        """BodyのパラメータにimageUrlが存在しない場合は400エラーを返す."""
        result = post.handler(missing_image_url_data, {})
        assert result.get('statusCode') == 400
        assert result.get('body') == '{"error_message": "\'imageUrl\' is a required property"}'

    def test_validation_body_missing_price(self, missing_price_data):
        """Bodyのパラメータにpriceが存在しない場合は400エラーを返す."""
        result = post.handler(missing_price_data, {})
        assert result.get('statusCode') == 400
        assert result.get('body') == '{"error_message": "\'price\' is a required property"}'

    def test_validation_body_missing_description(self, missing_description_data):
        """Bodyのパラメータにdescriptionが存在しない場合は400エラーを返す."""
        result = post.handler(missing_description_data, {})
        assert result.get('statusCode') == 400
        assert result.get('body') == '{"error_message": "\'description\' is a required property"}'

    def test_correct_body(self, correct_input_data):
        """Bodyのパラメータが正常な場合はDBに登録しては201を返す."""
        result = post.handler(correct_input_data, {})

        body = parse_body(result.get('body'))
        dynamodb = boto3.resource('dynamodb', endpoint_url=os.environ['DynamoDBEndpoint'])
        products_table = dynamodb.Table(os.getenv('ProductsTableName'))
        response = products_table.get_item(Key={
            'Id': body.get('product_id'),
            'Key': 'info',
        })

        assert result.get('statusCode') == 201
        assert response.get('Item').get('Name') == 'ヘルメット'
        assert response.get('Item').get('Description') == '3'
        assert response.get('Item').get('Price') == '3000'
        assert response.get('Item').get('ImageUrl') == 'http://example.com'
