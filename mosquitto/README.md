# テスト用MQTTブローカ

ローカルPCでテストできるように、`docker-compose.yml`を用意しました。

## 事前準備

- Docker CE for Windows(Docker Desktop Community) をインストール
   動作確認は 2.2.0-win81(29211) で行いました。

## 起動

1. PowerShellを管理者として実行
2. `mosquitto` ディレクトリへ移動
3. `docker-compose up -d`

Mosquittoサーバが起動します。このサーバには、認証なしで接続できます。

## ログ表示

1. PowerShellを管理者として実行
2. `mosquitto` ディレクトリへ移動
3. `docker-compose logs -f`
   publish/subscribeされるとログ上に表示されます。
   
> 動作確認する場合は、この状態で `test_mqtt.py` を実行してください。

停止するには Ctrl + C を押してください。

## 停止

1. PowerShellを管理者として実行
2. `mosquitto` ディレクトリへ移動
3. `docker-compose stop`
4. `docker-compose rm -f`

## ライセンス

本ディレクトリ以下のコンテンツはすべて [MITライセンス](../LICENSE) 準拠とします。


