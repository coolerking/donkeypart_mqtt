# -*- coding: utf-8 -*-
"""
IBM Watson IoT Platform をつかったMQTTクライアントの具現クラス群を提供する。

- TubPublisher
   tubデータのJSON分のみMQTTサーバへpublishするクライアントクラス。
   Vehiecleフレームワークへadd可能なpartクラスでもある。

- PilotSubscriber
   AI実装の代わりにMQTTサーバから、指示をDonkeyCarへ送るためのSubscriberクラス。
   Vehiecleフレームワークへadd可能なpartクラスでもある。
   少なくともイメージデータをMQTTサーバへ送信していないと判断できないので
   本クラスはあくまで参考で実装したものである。
"""

from client import BaseClient, BrokerConfig
from tub import Message

BROKER = 'ibm'
KEY_CLIENT_ID = 'client_id'
KEY_HOST = 'host'
KEY_PORT = 'port'
KEY_USER = 'user'
KEY_PASSWORD = 'password'
KEY_PUB_TOPIC = 'pub_topic'
KEY_SUB_TOPIC = 'sub_topic'

class TubPublisher(BaseClient):
    """
    tubデータのJSON分のみMQTTサーバへpublishするクライアントクラス。
    Vehiecleフレームワークへadd可能なpartクラスでもある。
    """
    def __init__(self, config_path='mqtt/brokers.yml', stage='test', debug=False):
        """
        Mosquittoクライアントを初期化するための情報を設定ファイルから読み込み、
        親クラスのコンストラクタを使って初期化する。
        トピック名の取得元が異なる。

        引数
            config_path     設定ファイルのパス
            stage           ステージ名
            debug           デバッグモード
        戻り値
            なし
        """
        config = BrokerConfig(BROKER, stage)

        client_id = config.get_value(BROKER, stage, KEY_CLIENT_ID)
        host = config.get_value(BROKER, stage, KEY_HOST)
        port = config.get_value(BROKER, stage, KEY_PORT)
        if port is not None:
            port = int(port)
        user = config.get_value(BROKER, stage, KEY_USER)
        password = config.get_value(BROKER, stage, KEY_PASSWORD)
        
        # publish時に使用するトピック名
        self.topic = config.get_value(BROKER, stage, KEY_PUB_TOPIC)

        super().__init__(host=host, port=port, client_id=client_id, user=user, password=password)
    
    def run(self, user_throttle, user_angle, cam_image_array, user_mode, timestamp):
        """
        Vehicleフレームワークより呼び出されるメソッド。
        非同期で書き込まれるインスタンス変数の情報をVehiecleフレームワークへ渡すだけの処理。
        IoT Pに合わせた編集を加えている。

        引数
        """
        msg_dict = Message(user_throttle, user_angle, cam_image_array, user_mode, timestamp)
        ibm_msg_dict = { 'd': msg_dict }
        super().publish(self.topic, ibm_msg_dict)
    
    def shutdown(self):
        super().disconnect()


class PilotSubscriber(BaseClient):
    """
    AI実装の代わりにMQTTサーバから、指示をDonkeyCarへ送るためのSubscriberクラス。
    Vehiecleフレームワークへadd可能なpartクラスでもある。
    少なくともイメージデータをMQTTサーバへ送信していないと判断できないので
    本クラスはあくまで参考で実装したものである。
    """
    # pilot/angle, pilot/throttle
    PILOT_ANGLE = 'pilot/angle'
    PILOT_THROTTLE = 'pilot/throttle'

    def __init__(self, config_path='mqtt/brokers.yml', stage='test', debug=False):
        """
        Mosquittoクライアントを初期化するための情報を設定ファイルから読み込み、
        親クラスのコンストラクタを使って初期化する。
        トピック名の取得元が異なる。

        引数
            config_path     設定ファイルのパス
            stage           ステージ名
            debug           デバッグモード
        戻り値
            なし
        """
        config = BrokerConfig(BROKER, stage)

        client_id = config.get_value(BROKER, stage, KEY_CLIENT_ID)
        host = config.get_value(BROKER, stage, KEY_HOST)
        port = config.get_value(BROKER, stage, KEY_PORT)
        if port is not None:
            port = int(port)
        user = config.get_value(BROKER, stage, KEY_USER)
        password = config.get_value(BROKER, stage, KEY_PASSWORD)
        
        # subscribe時に使用するトピック名
        self.topic = config.get_value(BROKER, stage, KEY_SUB_TOPIC)

        self.pilot_angle = 0.0
        self.pilot_throttle = 0.0

        super().__init__(host=host, port=port, client_id=client_id, user=user, password=password)

    def run(self):
        """
        Vehicleフレームワークより呼び出されるメソッド。
        非同期で書き込まれるインスタンス変数の情報をVehiecleフレームワークへ渡すだけの処理。

        引数
            なし
        戻り値
            pilot_angle     アングル値
            pilot_throttle  スロットル値
        """
        if self.debug:
            print('[run] return pilot/angle:{}, pilot/throttle:{}'.format(
                str(self.pilot_angle), str(self.pilot_throttle)) )
        return self.pilot_angle, self.pilot_throttle

    def on_message(self, payload):
        """
        Pahoフレームワークより呼び出されるメソッド。
        購読メッセージが到着したら、インスタンス変数へ反映する。
        このクラスではVehicleのマルチスレッド機能を使用せず、
        Paho側のコールバックを利用している。

        引数
            payload     購読メッセージ
        戻り値
            なし
        """
        # アングルの更新
        pilot_angle = payload[self.PILOT_ANGLE]
        if pilot_angle is not None:
            self.pilot_angle = float(pilot_angle)
            if self.debug:
                print('update pilot/angle:' + str(self.pilot_angle))
        # スロットルの更新
        pilot_throttle = payload[self.PILOT_THROTTLE]
        if pilot_throttle is not None:
            self.pilot_throttle = float(pilot_throttle)
            if self.debug:
                print('update pilot/throttle: ' + str(self.pilot_throttle))
