# -*- coding: utf-8 -*-
import numpy as np
from getch import getch


def input_keys(size=30):
    ## -----*----- 連続キーを入力 -----*----- ##
    keys = np.zeros(size)

    for i in range(size):
        key = getch()
        keys[i] = int(key.encode('utf-8', 'replace').hex(), 16)

        # 入力終了
        if key == '\n':
            break

    return keys
