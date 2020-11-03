import tensorflow as tf
import pandas as pd
from numpy import reshape, array
import random

# setup initial params on calling
BODY_model_path = 'training/models/LSTM_Bidirectional_64x4_no_lookback_200epochs-3in-3out_model.h5'
BODY_model = tf.keras.models.load_model(BODY_model_path)


class Predictions():
    """will make predictions using RNN as both LSTM and audio_in"""
    def __init__(self):
        # set up global variables
        print('ml ready')

    def seed(self, data_list):
        # randomly generate a starting seed
        seed = random.choice(data_list)
        print('seed   ===  ', seed)

        # passes seed to df prep
        ml_seed = self.make_df(seed)
        return ml_seed

    def make_df(self, incoming):
        # takes incoming tuple and converts into self.df for ml
        df = pd.DataFrame([incoming], columns=["x", "y", "z"])
        df = df.filter(['x', 'y', 'z'])
        # print(df)
        return df

    # functions producing data
    def ml_predictions(self, features): # RNN predict x, y, z
        # converts incoming tuple into array
        row = array(features)

        # reshapes array into 2 dimensions for tf predict
        inputX = reshape(row, (row.shape[0], row.shape[1], 1))

        # makes a predictaion
        pred = BODY_model.predict(inputX, verbose=0)

        # parses it and returns ias individual vars
        pred_x, pred_y, pred_z = pred[0,0], pred[0,1], pred[0,2]
        return (pred_x, pred_y, pred_z)

