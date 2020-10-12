from keras.models import load_model
from random import shuffle, randrange
import pandas as pd
from numpy import reshape, array
from time import sleep
import os
#from jetbot import Robot

# load models from single files
BODY_model_path = 'training/models/LSTM_Bidirectional_64x4_no_lookback_body_full-dataset_200epochs-3in-3out_model.h5'
BODY_model = load_model(BODY_model_path)
test_dataset_path = 'training/good_dataset_mini.csv'


def ml_predictions(features):
    row = array(features)
    inputX = reshape(row, (row.shape[0], row.shape[1], 1))
    pred = BODY_model.predict(inputX, verbose=0)
    pred_x, pred_y = pred[0,0], pred [0,1]
    # print('prediction RNN = ', pred)
    robot_move(pred_x, pred_y)

def robot_move(pred_x, pred_y):
    multi_factor = 2
    pred_x *= multi_factor # todo rescale rather than blanket * x
    pred_y *= multi_factor
    left_wheel_move, right_wheel_move = 0, 0
    # left and right motion
    if pred_x < 0:
        right_wheel_move += pred_x * -1
    else:
        left_wheel_move += pred_x
    # fwd & bwd motion
    right_wheel_move += pred_y
    left_wheel_move += pred_y
    print(left_wheel_move, right_wheel_move)
    #robot.set_motors(left_wheel_move, right_wheel_move)


df = pd.read_csv(test_dataset_path, sep=",", header=None, names=["id", "limb", "x", "y", "z", "freq", "amp"])
df = df.filter(['x', 'y', 'z'])
print(df)
index = list(df.index)
shuffle(index)
df = df.iloc[index]
df.reset_index()

# robot = Robot()

# iterate through each row
for ind in df.index:
    if ind % 10 == 0:
        row = [[df['x'][ind], df['y'][ind], df['z'][ind]]]
        # rowdf = df.filter(['x', 'y', 'z',  = row[0,0:3]
        # print (row)
        ml_predictions(row)
        sleep_rnd = randrange(2)
        sleep(sleep_rnd)


