import yaml
from lib.keyhundle import *
from lib.predict import LSTM_


infer = LSTM_(train=False)
config = yaml.load(open('config/param.yaml'), Loader=yaml.SafeLoader)

hundler = Hundle(config['size'])
while True:
    print('\n===== キーを入力してください ======')
    data = hundler.input_keys()
    print('入力文字：%s' % infer.predict(data=data)[0])
