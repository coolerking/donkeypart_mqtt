# -*- coding: utf-8 -*-
"""
tubデータを扱うためのクラス。
"""

class Record:
    """
    tubデータのrecordファイルの1ファイルをあらわすクラス。
    辞書データ化が簡単になる。
    """
    # JSONデータとなる定数
    USER_THROTTLE = 'user/throttle'
    USER_ANGLE = 'user/angle'
    CAM_IMAGE_ARRAY = 'cam/image_array'
    USER_MODE = 'user/mode'
    TIMESTAMP = 'timestamp'

    def __init__(self, user_throttle, user_angle, cam_image_array, user_mode, timestamp):
        self.user_throttle = user_throttle
        self.user_angle = user_angle
        self.cam_image_array = cam_image_array
        self.user_mode = user_mode
        self.timestamp = timestamp
    
    def get_dict(self):
        ret = {}
        ret[self.USER_THROTTLE] = self.user_throttle
        ret[self.USER_ANGLE] = self.user_angle
        ret[self.CAM_IMAGE_ARRAY] = self.cam_image_array
        ret[self.USER_MODE] = self.user_mode
        ret[self.TIMESTAMP] = self.timestamp
        return ret