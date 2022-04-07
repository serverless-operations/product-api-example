"""フィクスチャ."""
import os
import boto3
import pytest


@pytest.fixture(scope='session', autouse=True)
def setup_teardown():
    os.environ['ProductsTableName'] = 'Products'
    os.environ['DynamoDBEndpoint'] = 'http://localhost:8435'
    """テストの前にテーブル名を環境変数に展開."""
    create_products_table()
    yield
    delete_products_table()


def delete_products_table():
    dynamodb = boto3.client('dynamodb', endpoint_url=os.environ['DynamoDBEndpoint'])
    dynamodb.delete_table(
        TableName=os.environ['ProductsTableName']
    )


def create_products_table():
    print(os.environ.get('ProductsTableName'))
    dynamodb = boto3.resource('dynamodb', endpoint_url=os.environ['DynamoDBEndpoint'])
    dynamodb.create_table(
        TableName=os.environ['ProductsTableName'],
        KeySchema=[
            {
                'AttributeName': 'Id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'Key',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Key',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Value',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        },
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'SearchIndex',
                'KeySchema': [
                    {
                        'AttributeName': 'Key',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'Value',
                        'KeyType': 'RANGE'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 123,
                    'WriteCapacityUnits': 123
                }
            },
        ]
    )


@pytest.fixture
def correct_input_data():
    return {
        "version": "2.0",
        "routeKey": "POST /products",
        "rawPath": "/products",
        "rawQueryString": "",
        "headers": {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "authorization": "Bearer eyJhbGciOiJ",
            "content-length": "151",
            "content-type": "application/json",
            "host": "799dcg9vr4.execute-api.ap-northeast-1.amazonaws.com",
            "postman-token": "1517b9b6-b3be-4eee-b077-e8631e4498d4",
            "user-agent": "PostmanRuntime/7.28.4",
            "x-amzn-trace-id": "Root=1-619271b9-6228738e52661cc90acb561b",
            "x-forwarded-for": "61.194.146.83",
            "x-forwarded-port": "443",
            "x-forwarded-proto": "https"
        },
        "requestContext": {
            "accountId": "825880940331",
            "apiId": "799dcg9vr4",
            "authorizer": {
                "jwt": {
                    "claims": {
                        "aud": "rFJiMc4eRhQ9uXsbkcoT4LEIiYyUVWBo",
                        "email": "horike@serverless.co.jp",
                        "email_verified": "true",
                        "exp": "1637023259",
                        "iat": "1636987259",
                        "iss": "https://product-api.jp.auth0.com/",
                        "name": "horike@serverless.co.jp",
                        "nickname": "horike",
                        "nonce": "VW9TcGZkYX5Hd1JrUFZ5NkJFSEVSZ2pwTEUyYnY4WkpteFJNZC0ydjVvcg==",
                        "picture": "https://s.gravatar.com/avatar/2ee9db3a5b6c492acf66ec14c8a5d8dc?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fho.png",
                        "sub": "auth0|618dd25edf74f6006bd6de9e",
                        "updated_at": "2021-11-15T14:40:58.196Z"
                    },
                    "scopes": None
                }
            },
            "domainName": "799dcg9vr4.execute-api.ap-northeast-1.amazonaws.com",
            "domainPrefix": "799dcg9vr4",
            "http": {
                "method": "POST",
                "path": "/products",
                "protocol": "HTTP/1.1",
                "sourceIp": "61.194.146.83",
                "userAgent": "PostmanRuntime/7.28.4"
            },
            "requestId": "I2a1BgZBNjMEJJw=",
            "routeKey": "POST /products",
            "stage": "$default",
            "time": "15/Nov/2021:14:42:01 +0000",
            "timeEpoch": 1636987321558
        },
        "body": {
            "name": 'ヘルメット',
            "imageUrl": "http://example.com",
            "price": "3000",
            "description": "3"
        },
        "isBase64Encoded": False
    }


@pytest.fixture
def missing_name_data():
    return {
        "version": "2.0",
        "routeKey": "POST /products",
        "rawPath": "/products",
        "rawQueryString": "",
        "headers": {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "authorization": "Bearer eyJhbG",
            "content-length": "151",
            "content-type": "application/json",
            "host": "799dcg9vr4.execute-api.ap-northeast-1.amazonaws.com",
            "postman-token": "1517b9b6-b3be-4eee-b077-e8631e4498d4",
            "user-agent": "PostmanRuntime/7.28.4",
            "x-amzn-trace-id": "Root=1-619271b9-6228738e52661cc90acb561b",
            "x-forwarded-for": "61.194.146.83",
            "x-forwarded-port": "443",
            "x-forwarded-proto": "https"
        },
        "requestContext": {
            "accountId": "825880940331",
            "apiId": "799dcg9vr4",
            "authorizer": {
                "jwt": {
                    "claims": {
                        "aud": "rFJiMc4eRhQ9uXsbkcoT4LEIiYyUVWBo",
                        "email": "horike@serverless.co.jp",
                        "email_verified": "true",
                        "exp": "1637023259",
                        "iat": "1636987259",
                        "iss": "https://product-api.jp.auth0.com/",
                        "name": "horike@serverless.co.jp",
                        "nickname": "horike",
                        "nonce": "VW9TcGZkYX5Hd1JrUFZ5NkJFSEVSZ2pwTEUyYnY4WkpteFJNZC0ydjVvcg==",
                        "picture": "https://s.gravatar.com/avatar/2ee9db3a5b6c492acf66ec14c8a5d8dc?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fho.png",
                        "sub": "auth0|618dd25edf74f6006bd6de9e",
                        "updated_at": "2021-11-15T14:40:58.196Z"
                    },
                    "scopes": None
                }
            },
            "domainName": "799dcg9vr4.execute-api.ap-northeast-1.amazonaws.com",
            "domainPrefix": "799dcg9vr4",
            "http": {
                "method": "POST",
                "path": "/products",
                "protocol": "HTTP/1.1",
                "sourceIp": "61.194.146.83",
                "userAgent": "PostmanRuntime/7.28.4"
            },
            "requestId": "I2a1BgZBNjMEJJw=",
            "routeKey": "POST /products",
            "stage": "$default",
            "time": "15/Nov/2021:14:42:01 +0000",
            "timeEpoch": 1636987321558
        },
        "body": {
            "imageUrl": "http://example.com",
            "price": "3000",
            "description": "3"
        },
        "isBase64Encoded": False
    }


@pytest.fixture
def missing_image_url_data():
    return {
        "version": "2.0",
        "routeKey": "POST /products",
        "rawPath": "/products",
        "rawQueryString": "",
        "headers": {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "authorization": "Bearer eyJhbGciOiJ",
            "content-length": "151",
            "content-type": "application/json",
            "host": "799dcg9vr4.execute-api.ap-northeast-1.amazonaws.com",
            "postman-token": "1517b9b6-b3be-4eee-b077-e8631e4498d4",
            "user-agent": "PostmanRuntime/7.28.4",
            "x-amzn-trace-id": "Root=1-619271b9-6228738e52661cc90acb561b",
            "x-forwarded-for": "61.194.146.83",
            "x-forwarded-port": "443",
            "x-forwarded-proto": "https"
        },
        "requestContext": {
            "accountId": "825880940331",
            "apiId": "799dcg9vr4",
            "authorizer": {
                "jwt": {
                    "claims": {
                        "aud": "rFJiMc4eRhQ9uXsbkcoT4LEIiYyUVWBo",
                        "email": "horike@serverless.co.jp",
                        "email_verified": "true",
                        "exp": "1637023259",
                        "iat": "1636987259",
                        "iss": "https://product-api.jp.auth0.com/",
                        "name": "horike@serverless.co.jp",
                        "nickname": "horike",
                        "nonce": "VW9TcGZkYX5Hd1JrUFZ5NkJFSEVSZ2pwTEUyYnY4WkpteFJNZC0ydjVvcg==",
                        "picture": "https://s.gravatar.com/avatar/2ee9db3a5b6c492acf66ec14c8a5d8dc?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fho.png",
                        "sub": "auth0|618dd25edf74f6006bd6de9e",
                        "updated_at": "2021-11-15T14:40:58.196Z"
                    },
                    "scopes": None
                }
            },
            "domainName": "799dcg9vr4.execute-api.ap-northeast-1.amazonaws.com",
            "domainPrefix": "799dcg9vr4",
            "http": {
                "method": "POST",
                "path": "/products",
                "protocol": "HTTP/1.1",
                "sourceIp": "61.194.146.83",
                "userAgent": "PostmanRuntime/7.28.4"
            },
            "requestId": "I2a1BgZBNjMEJJw=",
            "routeKey": "POST /products",
            "stage": "$default",
            "time": "15/Nov/2021:14:42:01 +0000",
            "timeEpoch": 1636987321558
        },
        "body": {
            "name": "ヘルメット",
            "price": "3000",
            "description": "3"
        },
        "isBase64Encoded": False
    }


@pytest.fixture
def missing_price_data():
    return {
        "version": "2.0",
        "routeKey": "POST /products",
        "rawPath": "/products",
        "rawQueryString": "",
        "headers": {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "authorization": "Bearer eyJhbGciOiJ",
            "content-length": "151",
            "content-type": "application/json",
            "host": "799dcg9vr4.execute-api.ap-northeast-1.amazonaws.com",
            "postman-token": "1517b9b6-b3be-4eee-b077-e8631e4498d4",
            "user-agent": "PostmanRuntime/7.28.4",
            "x-amzn-trace-id": "Root=1-619271b9-6228738e52661cc90acb561b",
            "x-forwarded-for": "61.194.146.83",
            "x-forwarded-port": "443",
            "x-forwarded-proto": "https"
        },
        "requestContext": {
            "accountId": "825880940331",
            "apiId": "799dcg9vr4",
            "authorizer": {
                "jwt": {
                    "claims": {
                        "aud": "rFJiMc4eRhQ9uXsbkcoT4LEIiYyUVWBo",
                        "email": "horike@serverless.co.jp",
                        "email_verified": "true",
                        "exp": "1637023259",
                        "iat": "1636987259",
                        "iss": "https://product-api.jp.auth0.com/",
                        "name": "horike@serverless.co.jp",
                        "nickname": "horike",
                        "nonce": "VW9TcGZkYX5Hd1JrUFZ5NkJFSEVSZ2pwTEUyYnY4WkpteFJNZC0ydjVvcg==",
                        "picture": "https://s.gravatar.com/avatar/2ee9db3a5b6c492acf66ec14c8a5d8dc?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fho.png",
                        "sub": "auth0|618dd25edf74f6006bd6de9e",
                        "updated_at": "2021-11-15T14:40:58.196Z"
                    },
                    "scopes": None
                }
            },
            "domainName": "799dcg9vr4.execute-api.ap-northeast-1.amazonaws.com",
            "domainPrefix": "799dcg9vr4",
            "http": {
                "method": "POST",
                "path": "/products",
                "protocol": "HTTP/1.1",
                "sourceIp": "61.194.146.83",
                "userAgent": "PostmanRuntime/7.28.4"
            },
            "requestId": "I2a1BgZBNjMEJJw=",
            "routeKey": "POST /products",
            "stage": "$default",
            "time": "15/Nov/2021:14:42:01 +0000",
            "timeEpoch": 1636987321558
        },
        "body": {
            "name": "ヘルメット",
            "imageUrl": "http://example.com",
            "description": "3"
        },
        "isBase64Encoded": False
    }


@pytest.fixture
def missing_description_data():
    return {
        "version": "2.0",
        "routeKey": "POST /products",
        "rawPath": "/products",
        "rawQueryString": "",
        "headers": {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "authorization": "Bearer eyJhbGciOiJ",
            "content-length": "151",
            "content-type": "application/json",
            "host": "799dcg9vr4.execute-api.ap-northeast-1.amazonaws.com",
            "postman-token": "1517b9b6-b3be-4eee-b077-e8631e4498d4",
            "user-agent": "PostmanRuntime/7.28.4",
            "x-amzn-trace-id": "Root=1-619271b9-6228738e52661cc90acb561b",
            "x-forwarded-for": "61.194.146.83",
            "x-forwarded-port": "443",
            "x-forwarded-proto": "https"
        },
        "requestContext": {
            "accountId": "825880940331",
            "apiId": "799dcg9vr4",
            "authorizer": {
                "jwt": {
                    "claims": {
                        "aud": "rFJiMc4eRhQ9uXsbkcoT4LEIiYyUVWBo",
                        "email": "horike@serverless.co.jp",
                        "email_verified": "true",
                        "exp": "1637023259",
                        "iat": "1636987259",
                        "iss": "https://product-api.jp.auth0.com/",
                        "name": "horike@serverless.co.jp",
                        "nickname": "horike",
                        "nonce": "VW9TcGZkYX5Hd1JrUFZ5NkJFSEVSZ2pwTEUyYnY4WkpteFJNZC0ydjVvcg==",
                        "picture": "https://s.gravatar.com/avatar/2ee9db3a5b6c492acf66ec14c8a5d8dc?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fho.png",
                        "sub": "auth0|618dd25edf74f6006bd6de9e",
                        "updated_at": "2021-11-15T14:40:58.196Z"
                    },
                    "scopes": None
                }
            },
            "domainName": "799dcg9vr4.execute-api.ap-northeast-1.amazonaws.com",
            "domainPrefix": "799dcg9vr4",
            "http": {
                "method": "POST",
                "path": "/products",
                "protocol": "HTTP/1.1",
                "sourceIp": "61.194.146.83",
                "userAgent": "PostmanRuntime/7.28.4"
            },
            "requestId": "I2a1BgZBNjMEJJw=",
            "routeKey": "POST /products",
            "stage": "$default",
            "time": "15/Nov/2021:14:42:01 +0000",
            "timeEpoch": 1636987321558
        },
        "body": {
            "name": "ヘルメット",
            "imageUrl": "http://example.com",
            "price": "3000"
        },
        "isBase64Encoded": False
    }
