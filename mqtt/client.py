# -*- coding: utf-8 -*-
"""
MQTTクライアントの基底オブジェクトを提供する。
paho-mqttパッケージを使用しているため、利用する場合は
インストールが必要となる。
"""
import os
import json
import yaml
import paho.mqtt.client as mqtt

class BaseClient:
    """
    MQTTクライアント基底クラス。
    本クラスはpublisher、subscriber両方の機能を内包しているため、
    どちらかの機能に特化したサブクラスを作成することを推奨する。
    """

    def __init__(self, 
    host, port=None, keepalive=None,
    client_id=None, protocol=mqtt.MQTTv311, 
    user=None, password=None,
    debug=False):
        """
        （共通）インスタンス変数を初期化する。
        インスタンス化された時点でクライアントオブジェクトは生成されるが、
        接続は行わない。

        引数
            host            ブローカのホスト名（必須）
            port            ブローカと接続するポート（デフォルトはNone）
            client_id       クライアントID（使用しないブローカの場合は指定しない）
            protocol        プロトコル名（デフォルトはNone）
            keepalive       接続確認を行う間隔
            user            ユーザ（認証しない場合は指定しない）
            passowrd        パスワード（認証しない場合は指定しない）
            debug           デバッグモード（デフォルトはFalse）
        戻り値
            なし
        """
        self.debug = debug

        if host is None:
            raise Exception('cannot connect mqtt host')
        self.host = host
        if port is not None:
            port = int(port)
        self.port = port
        if keepalive is not None:
            keepalive = int(keepalive)
        self.keepalive = keepalive

        # MQTT clientのインスタンス化
        self.client = self.get_client(client_id, protocol)
        
        # 認証情報のセット
        self._set_auth(user, password)


    def get_client(self, client_id, protocol):
        """
        （共通）MQTTブローカクライアントオブジェクトを生成する。

        引数
            client_id       クライアントID（使用しないブローカの場合は指定しない）
            protocol        プロトコル名（デフォルトはNone）
        戻り値
            client          MQTTブローカクライアント
        """
        if client_id is None and protocol is None:
            client = mqtt.Client()
            if self.debug:
                print('client instantiate')
        elif client_id is None and protocol is not None:
            client = mqtt.Client(protocol=protocol)
            if self.debug:
                print('client instantiate with protocol')
        elif client_id is not None and protocol is None:
            client = mqtt.Client(client_id)
            if self.debug:
                print('client instantiate client_id=' + client_id)
        else:
            client = mqtt.Client(client_id, protocol=protocol)
            if self.debug:
                print('client instantiate client_id=' + client_id + ' with protocol')
        return client

    def _set_auth(self, user, password):
        """
        （共通）認証情報をクライアントオブジェクトにセットする。

        引数
            user            ユーザ（認証しない場合は指定しない）
            passowrd        パスワード（認証しない場合は指定しない）
        戻り値
            なし
        """
        if user is not None and password is not None:
            self.client.username_pw_set(user, password)
            if self.debug:
                print('set user=' + user + ', password=' + password)



    def _connect(self):
        """
        （共通）インスタンス変数に格納された情報をもとにMQTTブローカへ接続する。

        引数
            なし
        戻り値
            なし
        """
        if self.port is None and self.keepalive is None:
            self.client.connect(self.host)
        elif self.port is None and self.keepalive is not None:
            self.client.connect(self.host, keepalive=self.keepalive)
        elif self.port is not None and self.keepalive is None:
            self.client.connect(self.host, port=self.port)
        else:
            print(type(self.port))
            self.client.connect(self.host, port=self.port, keepalive=self.keepalive)
        if self.debug:
            print('connect to mqtt broker')
    
    def subscribe(self, topic):
        """
        (サブスクライバ)サブスクライバとして待ち受けを開始する。
        コールバック関数を登録し、MQTTブローカと接続した後、
        クライアントを待ち受けループ状態にする。
        停止させたい場合は、disconnect()を呼び出す。

        引数
            topic           購読するトピック名
        戻り値
            なし
        """
        self.topic = topic
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        if self.debug:
            print('set callback functions')
        self._connect()
        self.client.loop_start()
        if self.debug:
            print('loop thread started')
        if self.debug:
            print('start loop for subscriber')

    def unsubscribe(self):
        self.client.loop_stop()
        if self.debug:
            print('loop thread stoped')


    def _on_connect(self, client, userdata, flags, response_code):
        """
        （サブスクライバ）接続時コールバック関数。
        トピックの購読を開始する。

        引数
            client
            userdata
            flags
            response_code
        戻り値
            なし
        """
        if self.debug:
            print('on connect code=' + str(response_code))
        client.subscribe(self.topic)
        if self.debug:
            print('subscribe topic=' + self.topic)

    def _on_message(self, client, userdata, msg):
        """
        （サブスクライバ）購読メッセージ受領時コールバック関数。
        購読メッセージを文字列化してテンプレートメソッドon_messageを呼び出す。

        引数
            client
            userdata
            msg
        戻り値
            なし
        """
        body = msg.payload.decode()
        self.payload = json.loads(body)
        if self.debug:
            print('msg.payload: ' + body)
        self.on_message(self.payload)
    
    def on_message(self, payload):
        """
        （サブスクライバ）購読メッセージを受領したら本メソッドが呼び出される。
        本メソッドの実装はないためなにもしないが、サブスクライバサブクラスでは
        本メソッドをオーバライドしてインスタンス変数に値を格納する。

        引数
            payload     メッセージ（JSONオブジェクト）
        戻り値
            なし
        """
        if self.debug:
            print('no operation in on_message template method')


    def publish(self, topic, msg_dict):
        if topic is None:
            raise Exception('no topic')
        if msg_dict is None:
            raise Exception('no message')
        self._connect()
        self.client.publish(topic, json.dumps(msg_dict))
        if self.debug:
            print('publish topic: ' + topic + ',  message: ' + str(msg_dict))
        

    def disconnect(self):
        self.client.disconnect()
        if self.debug:
            print('disconnect mqtt broker')


class BrokerConfig:

    # テンプレートのタイプ名
    TEMPLATE = 'template' 


    def __init__(self, config_path='mqtt/brokers.yml', debug=False):
        """
        コンストラクタ。
        設定ファイルを読み込みインスタンス変数configへ格納する。

        引数
            conf_path   設定ファイルへのパス
            debug       デバッグモード
        戻り値
            なし
        """
        # デバッグモードの格納
        self.debug = debug
        # 設定ファイルの確認
        if config_path is None:
            raise Exception('no config path')
        path = os.path.expanduser(config_path)
        if not os.path.exists(path):
            raise Exception('no config file: ' + config_path)

        # 設定ファイル読み込み
        with open(path, 'r') as f:
            config = yaml.load(f)
        
        # ブローカ名リストibm,mosquitto
        self.brokers = list(config.keys())

        self.config = {}
        # ibm, mosq..
        for broker in self.brokers:
            # template, product, test..
            stages = list(config[broker].keys())
            # brokerの設定タイプ
            stage_config = {}
            for stage in stages:
                # template は書き方例なので飛ばす
                if stage == self.TEMPLATE:
                    continue
                # template以外は残す
                stage_config[stage] = (config[broker])[stage]
            self.config[broker] = stage_config
        
        if self.debug:
            print(self.config)

    def get_brokers(self):
        return list(self.config.keys())
    
    def get_stages(self, broker):
        brokers = self.get_brokers()
        if broker not in brokers:
            raise Exception('no broker:' + broker)
        return list((self.config[broker]).keys())

    def get_keys(self, broker, stage):
        stages = self.get_stages(broker)
        if stage not in stages:
            raise Exception('no stage:' + stage + ' in ' + broker)
        return list(((self.config[broker])[stage]).keys())

    def get_value(self, broker, stage, key):
        keys = self.get_keys(broker, stage)
        if key not in keys:
            raise Exception('no key:' + key + ' in ' + stage + ' in ' + broker)
        return ((self.config[broker])[stage])[key]


