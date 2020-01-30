import yaml
from lib.keyhundle import *
from lib.predict import LSTM_


infer = LSTM_(train=False)
config = yaml.load(open('config/param.yaml'), Loader=yaml.SafeLoader)

while True:
    print('\n\n===== キーを入力してください ======')
    data = input_keys(config['size'])
    print('入力文字：%s' % infer.predict(data=data)[0])
