## 事前にPC上にインストールが必要なもの
ローカル環境の状態に合わせて、以下のインストール状況を確認し、存在しなければインストールして下さい。
- Python3: Python3.9以上をインストール
- pip3: Pythonで使用するライブラリやツールを管理するパッケージマネージャー
- nodejs: Serverless Frameworkを実行するために必要
- yarn: Serverless Frameworkで使用するツールをインストールするために必要

## 初期セットアップ

ソースコードを展開してください。
```
$ git clone git@github.com:serverless-operations/product-api-example.git
$ cd product-api-example
$ export NODE_ENV=test && yarn install　#Serverless Framework関連のライブラリをインストール
$ export PYTHONPATH=./
```

Python 関連のライブラリのインストールします。venvを使用して環境を構築してください。 `requirements/dev.txt`には開発で使用するライブラリを記述します。本番で使用するライブラリは`requirements/prod.txt`にも記載してください。
```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip3 install -r requirements/dev.txt
```

ライブラリをインストールした際は以下の手順で`requirements`配下のファイルに記述します。
```
$ pip3 install flake8
$ pip3 freeze > requirements/dev.txt
```

## Lint

pep8というコーディング規約にそって構文チェックを行います
```
$ flake8
```

## テスト

pytestによる自動テストを行います。テストの前にDynamoDBのローカルコンテナを立ち上げてユニットテストからアクセスできるようにして下さい。

コンテナの起動
```
$ yarn start
```

テストの実行
```
$ pytest -s
```

## デプロイ

```
$ yarn serverless deploy --stage `ステージ名`
```

## ローカル開発

ローカルサーバーを起動する。AuthorizerにはServerless Offlineが対応して使えないので注意が必要
```
$ yarn serverless offline --noAuth 
```

## Pull Request Test
done!