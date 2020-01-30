# -*- coding: utf-8 -*-
'''
教師データをビルドするプログラム
　- コマンドライン引数に記録する文字を入力
　- config/class.yamlに各ビルド設定を記載
　- ビルド後のキー入力の系列データを保存
'''

import os
import sys
import shutil
import glob
import yaml
from tqdm import tqdm


if len(sys.argv) < 2:
    print('plese enter classs name!!')
    exit(0)


# クラスを登録
classes = yaml.load(open('config/class.yaml'), Loader=yaml.SafeLoader)
class_name = sys.argv[1]
if classes == None:
    classes = []
if not class_name in classes:
    classes.append(class_name)
    yaml.dump(classes, open('config/class.yaml', 'w'))
os.makedirs('data/' + class_name, exist_ok=True)

