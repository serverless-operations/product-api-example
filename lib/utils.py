"""全サービス共通で使うユーティリティ."""
import json
import logging
import decimal
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def parse_body(body):
    """リクエストBodyをパースする."""
    return json.loads(body)


def response_builder(status_code, body={}):
    """APIレスポンスを生成する."""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }


class DecimalEncoder(json.JSONEncoder):
    """JSONエンコーダー."""

    def default(self, obj):
        """エンコード処理."""
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)
