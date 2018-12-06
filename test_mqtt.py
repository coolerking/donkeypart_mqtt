# -*- coding: utf-8 -*-
"""
MQTTブローカとの通信テストを行います。

Usage:
    test_mqtt.py [--host <host>] [--port <port>] [--keepalive <keepalive>]

Options:
    --host HOSTNAME                 ホスト名
    --port PORT_NO                  ポート番号
    --keepalive INTERVAL_SECONDS    接続確認間隔
"""
import os
import docopt
from time import sleep
from mqtt.client import BaseClient

# トピック名
test_topic = 'check_mqtt/test'
# publishするメッセージ（辞書型）
test_msg = { 'd':{ 'text':'hehehe', 'number':123 }}


# テスト処理本体
if __name__ == '__main__':
    # 引数情報の収集
    args = docopt.docopt(__doc__)

    # ホスト名
    host = args['--host']
    if host is None:
        host = '127.0.0.1'

    # ポート番号
    port = args['--port']
    if port is None:
        port = 1883
    else:
        port = int(port)

    # 生存確認を行う間隔
    keepalive = args['--keepalive']
    if keepalive is None:
        keepalive = 60
    else:
        keepalive = int(keepalive)
    
    # ターゲットとなるMQTTブローカ情報
    print('target server host:{}, port:{}, keepalive:{}'.format(host, str(port), str(keepalive)))

    # サブスクライバを用意
    sub = BaseClient(host=host, port=port, keepalive=keepalive, debug=True)
    # 別スレッドで待ち受けており、subscribeされたらすぐにメッセージを表示する
    # このためベーススレッドでのprintと混ざって表示されることがある
    sub.subscribe(test_topic)

    # パブリッシャを用意
    pub = BaseClient(host=host, port=port, keepalive=keepalive, debug=True)
    # メッセージ送信1回目
    pub.publish(test_topic, test_msg)
    sleep(0.2)
    # メッセージ送信2回目
    pub.publish(test_topic, test_msg)
    sleep(0.2)
    # メッセージ送信3回目
    pub.publish(test_topic, test_msg)

    sleep(1.0)
    # 待受スレッドを停止
    sub.unsubscribe()
    # サブスクライバ側クライアントの接続を解除
    sub.disconnect()

    # パブリッシャ側クライアントの接続を解除
    pub.disconnect()