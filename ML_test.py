from keras.models import load_model
from random import shuffle
import pandas as pd
from numpy import reshape, array
from time import sleep
import os
from jetbot import Robot

# load models from single files
BODY_model_path = 'training/models/LSTM_Bidirectional_64x4_no_lookback_body_1000epochs-3in-3out_model.h5'
BODY_model = load_model(BODY_model_path)
test_dataset_path = 'training/good_dataset_mini.csv'


def ml_predictions(features):
    row = array(features)
    inputX = reshape(row, (row.shape[0], row.shape[1], 1))
    pred = BODY_model.predict(inputX, verbose=0)
    move_x, move_y = pred[0,0], pred [0,1] # garbage for now TODO translaet x and y to l/r & fwd/bwd
    if move_x < 0:
        robot.left(move_x * -1)
    else:
        robot.right(move_x)
    print('prediction RNN = ', pred)


df = pd.read_csv(test_dataset_path, sep=",", header=None, names=["id", "limb", "x", "y", "z", "freq", "amp"])
print(df)
index = list(df.index)
shuffle(index)
df = df.iloc[index]
df.reset_index()

robot = Robot()

# iterate through each row
for ind in df.index:
    if ind % 10 == 0:
        row = [[df['x'][ind], df['y'][ind], df['z'][ind], df['freq'][ind], df['amp'][ind]]]
        ml_predictions(row)
        sleep(0.1)


