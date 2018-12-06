# MQTT Publisher/Subscriber パーツライブラリ

Donkey Carが取得したセンサデータなどをMQTTブローカへpublishしたり、ローカルの機械学習モデルを使用しないでMQTTブローカから自動操縦データを受け取りたい場合に使用する基底クラスやサンプル具現クラスを提供します。

サンプル具現クラスでは、Donkey CarのVehicleフレームワークに従ってPublisher/Subscriberを実装しているので、`manage.py`を書き換えるだけで、`TubWriter`の一部や`KerasLinear`を置き換えることができます。


## MQTTブローカ

サンプル具現クラスは以下のMQTTブローカを前提としています。

- [Eclipse Mosquitto(Docker)](https://mosquitto.org/)
- [IBM Watson IoT Platform(IBM Cloud)](https://www.ibm.com/jp-ja/marketplace/internet-of-things-cloud)


## 基底クラス

|クラス名|ソースコード|説明|
|:-------------|:------------------|:--------|
| `BaseClient` | `mqtt/client.py` | 汎用MQTTクライアントクラス、IoTP/Mosquitto両方のパラメータに対応できるように実装している。ただしpartクラスとしてのメソッドは実装していない。|
| `BaseConfig` | `mqtt/client.py` | 設定ファイル(YAML型式)を操作するためのクラス。具現クラスを作成する際に利用できるように別途作成した。|
| `Record`     | `mqtt/tub.py`    | Donkey Carのtubデータのうちrecordファイルを表すクラス。1インスタンス1ファイルに相当する。 |

## サンプル具現クラス

### Eclipse Mosquitto Publisher/Subscriber

|クラス名|ソースコード|説明|
|:-------------|:------------------|:--------|
| `TubPublisher` | `mqtt/mosquitto.py` | Tubデータのうちのrecordファイルのみの情報をMQTTブローカへpuhlishするpartクラスサンプル。|
| `PilotSubscriber` | `mqtt/client.py` | モデルpartのかわりにMQTTブローカから操縦情報を取得するsubscriber partクラス。|
| テンプレート設定ファイル | `mqtt/brokers_template.yml` | ブローカ固有の設定を格納するための設定ファイルテンプレート。最上位からbroker、stage、keyとしてコードを実装している。template stageは、サンプルでありコード内でも無視するように記述されている。|
| mosquittoコンテナ | `mosquitto/docker-compose.yml` | テスト用のMosquittoコンテナを起動するためのDocker Composeファイル。Docker Desktop2.0.0で動作確認済み。`mosquitto`ディレクトリ内にはコンテナ起動に必要な設定ファイル等が入っている。|


### IBM Watson IoT Platform Publisher/Subscriber

|クラス名|ソースコード|説明|
|:-------------|:------------------|:--------|
| `TubPublisher` | `mqtt/ibm.py` | Tubデータのうちのrecordファイルのみの情報をMQTTブローカへpuhlishするpartクラスサンプル。|
| `PilotSubscriber` | `mqtt/ibm.py` | モデルpartのかわりにMQTTブローカから操縦情報を取得するsubscriber partクラス。|
| テンプレート設定ファイル | `mqtt/brokers_template.yml` | ブローカ固有の設定を格納するための設定ファイルテンプレート。最上位からbroker、stage、keyとしてコードを実装している。template stageは、サンプルでありコード内でも無視するように記述されている。|

> IBM Watson IoT Platform は　IBM Cloud より無料版(ライトプラン)が利用可能です。


## ライセンス

本リポジトリ上のコード、ドキュメントはすべて [MITライセンス](./LICENSE) 準拠とします。