# -*- coding: utf-8 -*-
'''
教師データをビルドするプログラム
　- コマンドライン引数に記録する文字を入力
　- config/class.yamlに各ビルド設定を記載
　- ビルド後のキー入力の系列データを保存
'''

import os
import sys
import yaml
import csv
import datetime
from lib.keyhundle import *


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
    yaml.dump(classes, open('config/class.yaml', 'w'), encoding='utf8')
os.makedirs('data/' + class_name, exist_ok=True)


# 入力キーを記録
print('「%s」を記録（Ctrl-Cで終了）' % class_name)
config = yaml.load(open('config/param.yaml'), Loader=yaml.SafeLoader)
hundler = Hundle(config['size'])
cnt = 0
while True:
    print('Now：%d step' % cnt)
    keys = hundler.input_keys()
    dt_now = datetime.datetime.now()
    file_name = 'data/%s/%s.csv' % (
        class_name,
        datetime.datetime.now().strftime('%Y-%m-%d--%H:%M:%S:%f')
    )

    # CSVに保存
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(keys)

    cnt += 1
