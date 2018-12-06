# -*- coding: utf-8 -*-
"""
ブローカ設定ファイルユーティリティのテストプログラム。

Usage:
    test_conf.py [--conf <file>] [--debug]

Options:
    --conf CONFIG_FILE_PATH     設定ファイルのパスを指定する
    --debug                     デバッグモード
"""
import os
import docopt
from mqtt.client import BrokerConfig

test_conf_path = 'mqtt/brokers.yml'


if __name__ == '__main__':
    # 引数情報の収集
    args = docopt.docopt(__doc__)

    # ホスト名
    conf_path = args['--conf']
    if conf_path is None:
        conf_path = test_conf_path
    
    debug = args['--debug']

    conf = BrokerConfig(conf_path, debug=debug)

    brokers = conf.get_brokers()
    for broker in brokers:
        print('broker: ' + broker)
        stages = conf.get_stages(broker)
        for stage in stages:
            print(' stage: ' + stage)
            keys = conf.get_keys(broker, stage)
            for key in keys:
                value = conf.get_value(broker, stage, key)
                print('  key:{}, value:{}'.format(key, str(value)))

    