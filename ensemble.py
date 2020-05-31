from __future__ import print_function
from sklearn.linear_model import LogisticRegression, LinearRegression
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.svm import LinearSVC, SVC
from sklearn import metrics
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import StandardScaler, Normalizer
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def prepare_data_per():
    malware = pd.read_csv('data/per_malware.csv')
    benign = pd.read_csv('data/per_benign.csv')
    data = pd.concat([malware, benign], ignore_index=True)
    data = data.sort_values(by=['name'])
    mal_list = pd.read_csv(
        'list_malware.csv', header=None).values[:-1].reshape(-1)
    beg_list = pd.read_csv(
        'list_benign.csv', header=None).values[:-1].reshape(-1)

    v_mal = int(len(mal_list) * 0.6)
    v_beg = int(len(beg_list) * 0.6)
    t_mal = int(len(mal_list) * 0.7)
    t_beg = int(len(beg_list) * 0.7)
    X_train = data[data['name'].isin(
        mal_list[:v_mal]) | data['name'].isin(beg_list[:v_beg])]
    y_train = X_train.values[:, -1].astype('int')
    X_train = X_train.values[:, 1:-1]

    X_val = data[data['name'].isin(
        mal_list[v_mal:t_mal]) | data['name'].isin(beg_list[v_beg:t_beg])]
    y_val = X_val.values[:, -1].astype('int')
    X_val = X_val.values[:, 1:-1]

    X_test = data[data['name'].isin(
        mal_list[t_mal:]) | data['name'].isin(beg_list[t_beg:])]
    y_test = X_test.values[:, -1].astype('int')
    X_test = X_test.values[:, 1:-1]

    X_train = np.array(X_train.reshape(-1, 20, 20), dtype='Float32')
    X_test = np.array(X_test.reshape(-1, 20, 20), dtype='Float32')
    X_val = np.array(X_val.reshape(-1, 20, 20), dtype='Float32')

    y_train = to_categorical(y_train, num_classes=2)
    y_val = to_categorical(y_val, num_classes=2)

    return X_train, y_train, X_test, y_test, X_val, y_val


def prepare_data_syscall(seed):
    data = pd.read_csv('data/syscall.csv')
    data = data.sort_values(by=['name'])
    mal_list = pd.read_csv(
        'list_malware.csv', header=None).values[:-1].reshape(-1)
    beg_list = pd.read_csv(
        'list_benign.csv', header=None).values[:-1].reshape(-1)

    v_mal = int(len(mal_list) * 0.6)
    v_beg = int(len(beg_list) * 0.6)
    t_mal = int(len(mal_list) * 0.7)
    t_beg = int(len(beg_list) * 0.7)

    X_train = data[data['name'].isin(
        mal_list[:v_mal]) | data['name'].isin(beg_list[:v_beg])]
    y_train = X_train.values[:, -1].astype('int')
    X_train = X_train.values[:, 1:-1]

    X_val = data[data['name'].isin(
        mal_list[v_mal:t_mal]) | data['name'].isin(beg_list[v_beg:t_beg])]
    y_val = X_val.values[:, -1].astype('int')
    X_val = X_val.values[:, 1:-1]

    X_test = data[data['name'].isin(
        mal_list[t_mal:]) | data['name'].isin(beg_list[t_beg:])]
    y_test = X_test.values[:, -1].astype('int')
    X_test = X_test.values[:, 1:-1]

    sfm = pickle.load(open('model/syscall_sfm.sav', 'rb'))
    X_train = sfm.transform(X_train)
    X_test = sfm.transform(X_test)
    X_val = sfm.transform(X_val)

    scaler = Normalizer()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    X_val = scaler.transform(X_val)

    return X_train, y_train, X_test, y_test, X_val, y_val


def prepare_data_net(seed):
    malware = pd.read_csv('data/net_malware.csv')
    benign = pd.read_csv('data/net_benign.csv')
    data = pd.concat([malware, benign], ignore_index=True)
    data = data.sort_values(by=['name'])
    mal_list = pd.read_csv(
        'list_malware.csv', header=None).values[:-1].reshape(-1)
    beg_list = pd.read_csv(
        'list_benign.csv', header=None).values[:-1].reshape(-1)

    t_mal = int(len(mal_list) * 0.7)
    t_beg = int(len(beg_list) * 0.7)
    v_mal = int(len(mal_list) * 0.6)
    v_beg = int(len(beg_list) * 0.6)
    X_train = data[data['name'].isin(
        mal_list[:v_mal]) | data['name'].isin(beg_list[:v_beg])]
    y_train = X_train.values[:, -1].astype('int')
    X_train = X_train.values[:, 1:-1]

    X_val = data[data['name'].isin(
        mal_list[v_mal:t_mal]) | data['name'].isin(beg_list[v_beg:t_beg])]
    y_val = X_val.values[:, -1].astype('int')
    X_val = X_val.values[:, 1:-1]

    X_test = data[data['name'].isin(
        mal_list[t_mal:]) | data['name'].isin(beg_list[t_beg:])]
    y_test = X_test.values[:, -1].astype('int')
    X_test = X_test.values[:, 1:-1]

    sfm = pickle.load(open('model/net_sfm.sav', 'rb'))
    X_train = sfm.transform(X_train)
    X_test = sfm.transform(X_test)
    X_val = sfm.transform(X_val)

    scaler = Normalizer()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    X_val = scaler.transform(X_val)

    return X_train, y_train, X_test, y_test, X_val, y_val


X_train_sys, y_train_sys, X_test_sys, y_test_sys, X_val_sys, y_val_sys = prepare_data_syscall(
    2020)
X_train_net, y_train_net, X_test_net, y_test_net, X_val_net, y_val_net = prepare_data_net(
    2020)
X_train_per, y_train_per, X_test_per, y_test_per, X_val_per, y_val_per = prepare_data_per()

lstm_per = Sequential()
lstm_per.add(LSTM(units=32, dropout=0.2,
                  recurrent_dropout=0.2, input_shape=(20, 20)))
lstm_per.add(Dense(2, activation='softmax'))
lstm_per.compile(loss='categorical_crossentropy',
                 optimizer=Adam(learning_rate=0.01), metrics=['accuracy'])
lstm_per.load_weights('model/per_lstm.h5')
clf_net = pickle.load(open('model/net_Random Forest.sav', 'rb'))
clf_sys = pickle.load(open('model/syscall_SVM.sav', 'rb'))

# Soft Voting
y_pred_net = clf_net.predict_proba(X_test_net)
y_pred_sys = clf_sys.predict_proba(X_test_sys)
y_pred_per = lstm_per.predict(X_test_per)

y_pred = (y_pred_net + y_pred_sys + y_pred_per) / 3
y_pred = np.argmax(y_pred, axis=1)
print(metrics.accuracy_score(y_test_net, clf_net.predict(X_test_net)))
print(metrics.accuracy_score(y_test_sys, clf_sys.predict(X_test_sys)))
print(metrics.accuracy_score(y_test_per, lstm_per.predict_classes(X_test_per)))
print(metrics.accuracy_score(y_test_net, y_pred))

y_pred_train_net = clf_net.predict_proba(X_train_net)[:, 0].reshape(-1, 1)
y_pred_train_sys = clf_sys.predict_proba(X_train_sys)[:, 0].reshape(-1, 1)
y_pred_train_per = lstm_per.predict(X_train_per)[:, 0].reshape(-1, 1)
y_pred_train = np.hstack(
    [y_pred_train_net, y_pred_train_sys, y_pred_train_per])

# Linear Regression
reg = LinearRegression(fit_intercept=False)
reg.fit(y_pred_train, y_train_sys)
y_pred_test = np.hstack([y_pred_net[:, 0].reshape(-1, 1),
                         y_pred_sys[:, 0].reshape(-1, 1),
                         y_pred_per[:, 0].reshape(-1, 1)])
y_pred_prob = reg.predict(y_pred_test)
y_pred = [y > 0.5 for y in y_pred_prob]
print(reg.coef_)
print(metrics.accuracy_score(y_test_net, y_pred))

# Logisic Regression
reg = LogisticRegression()
reg.fit(y_pred_train, y_train_sys)
y_pred = reg.predict(y_pred_test)
print(metrics.accuracy_score(y_test_net, y_pred))