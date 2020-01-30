# -*- coding: utf-8 -*-
import numpy as np
import time
from getch import getch


class Hundle():
    def __init__(self, size):
        ## -----*----- コンストラクタ -----*----- ##
        self.size = size
        self.reset()


    def reset(self):
        ## -----*----- ステータスをリセット -----*----- ##
        self.keys = np.zeros(self.size)
        self.is_end = False


    def input_keys(self, limit=1.0):
        ## -----*----- 連続キーを入力 -----*----- ##
        self.reset()
        t = time.time()

        for i in range(self.size):
            if time.time() - t > 1.0 and i >= 3:
                break
            t = time.time()

            key = getch()
            self.keys[i] = int(key.encode('utf-8', 'replace').hex(), 16)

        return self.keys
