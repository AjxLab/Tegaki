# -*- coding:utf-8 -*-
import os
import numpy as np
import yaml
import glob
from tqdm import tqdm
from tensorflow.keras.layers import Dense, LSTM, Dropout, Flatten
from tensorflow.keras import Sequential


class LSTM_():
    def __init__(self, train=False, model_path='./model/model.hdf5'):
        ## -----*----- コンストラクタ -----*----- ##
        self.classes = yaml.load(open('config/class.yaml'), Loader=yaml.SafeLoader)
        self.hparams = yaml.load(open('config/param.yaml'), Loader=yaml.SafeLoader)

        self.n_classes  = len(self.classes)
        self.batch_size = self.hparams['batch_size']
        self.epochs     = self.hparams['epochs']

        self.model_path = model_path

        # モデルのビルド
        self.__model = self.__build()

        if train:
            # 学習
            x, y = self.__features_extracter()
            self.__train(x, y)
        else:
            # モデルの読み込み
            self.load_model()


    def __build(self):
        ## -----*----- NNを構築 -----*----- ##
        # モデルの定義
        model = Sequential([
            #LSTM(256, input_shape=(self.hparams['size'], 1), activation='relu'),
            #Dropout(self.hparams['dropout']),
            Dense(256, input_shape=(self.hparams['size'],), activation='relu'),
            Dropout(self.hparams['dropout']),
            Dense(512, activation='relu'),
            Dropout(self.hparams['dropout']),
            Dense(256, activation='relu'),
            Dropout(self.hparams['dropout']),
            Dense(self.n_classes, activation='softmax')
        ])

        # モデルをコンパイル
        model.compile(
            optimizer=self.hparams['optimizer'],
            loss=self.hparams['loss'],
            metrics=['accuracy']
        )

        return model


    def __train(self, x, y):
        ## -----*----- 学習 -----*-----##
        print("\n\nTrain")
        self.__model.fit(x, y,  epochs=self.hparams['epochs'], batch_size=self.hparams['batch_size'])

        # 最終の学習モデルを保存
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        self.__model.save_weights(self.model_path)


    def __features_extracter(self):
        ## -----*----- 特徴量を抽出 -----*----- ##
        x = [] # 入力
        y = [] # 出力ラベル

        files = []
        for class_ in self.classes:
            class_files = [{'path': f, 'class': self.classes.index(class_)} for f in glob.glob('data/%s/*'%class_)]
            files.extend(class_files)

        for file in tqdm(files):
            x.append(self.__read_data(file['path']))
            y.append(file['class'])

        x = np.array(x, dtype=np.float32)
        #x = np.reshape(x, (x.shape[0], x.shape[1], 1))
        y = np.array(y, dtype=np.uint8)

        # ランダムに並べ替え
        perm = np.arange(len(x))
        np.random.shuffle(perm)
        x = x[perm]
        y = y[perm]

        return x, y


    def __read_data(self, file):
        ## -----*----- ファイルからデータを読み取り -----*----- ##
        csv_read = open(file, 'r').read().split(',')
        ret = map(lambda x: float(x), csv_read)

        return list(ret)


    def nomalize(self, x, axis=None):
        ## -----*----- 0~1に正規化 -----*----- ##
        x = np.array(x)
        min = x.min(axis=axis, keepdims=True)
        max = x.max(axis=axis, keepdims=True)
        if not (max - min) == 0:
            result = (x - min) / (max - min)
        else:
            result = x
        return result


    def load_model(self):
        ## -----*----- 学習済みモデルの読み込み -----*-----##
        # モデルが存在する場合，読み込む
        if os.path.exists(self.model_path):
            self.__model.load_weights(self.model_path)


    def predict(self, file=None, data=None):
        ## -----*----- 推論 -----*----- ##
        if not file == None:
            data = self.__read_data(file)
        score = self.__model.predict(np.array([data]), batch_size=None, verbose=0)
        pred = np.argmax(score)

        return self.classes[pred], score[0]
