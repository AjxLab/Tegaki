# -*- coding: utf-8 -*-
import numpy as np
import time
import threading
from getch import getch


class Hundle():
    def __init__(self, size):
        ## -----*----- コンストラクタ -----*----- ##
        self.size = size
        self.reset()

        threading.Thread(target=self.subT).start()


    def reset(self):
        ## -----*----- ステータスをリセット -----*----- ##
        self.keys = np.zeros(self.size)
        self.is_input = False
        self.is_end = False
        self.index = 0


    def input_keys(self, limit=0.7):
        ## -----*----- 連続キーを入力 -----*----- ##
        self.reset()
        t = time.time()

        while self.index < self.size:
            # ESCで終了
            if self.is_end:
                exit(0)

            if time.time() - t > limit:
                break

            if self.is_input:
                self.is_input = False
                t = time.time()

        print(self.keys)
        return self.keys


    def subT(self):
        ## -----*---- サブスレッド -----*----- ##
        while True:
            key = getch()
            key = int(key.encode('utf-8', 'replace').hex(), 16)
            if key == 27:
                break

            self.keys[self.index] = key
            self.index += 1
            self.index = self.index % self.size
            self.is_input = True

        self.is_end = True
