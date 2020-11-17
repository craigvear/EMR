import tensorflow as tf
import pandas as pd
from numpy import reshape, array
import random
import config
import time

# setup initial params on calling
BODY_model_path = 'training/models/LSTM_Bidirectional_64x4_no_lookback_200epochs-3in-3out_model.h5'
BODY_model = tf.keras.models.load_model(BODY_model_path)

AMP_model_path = 'training/models/LSTM_Bidirectional_64x4_no_lookback_200epochs-AMPin-XYout_model.h5'
AMP_model = tf.keras.models.load_model(AMP_model_path)

class Predictions():
    """will make predictions using RNN as both LSTM and audio_in"""
    debug_predict = False
    debug_parsing = False

    def __init__(self, glob_speed):
        # set up global variables
        print('ml ready')
        self.glob_speed = glob_speed

    def seed(self, data_list):
        # randomly generate a starting seed
        seed = random.choice(data_list)
        if self.debug_predict:
            print('seed   ===  ', seed)

        # passes seed to df prep
        ml_seed = self.make_df(seed)
        return ml_seed

    def make_df(self, incoming):
        # takes incoming tuple and converts into self.df for ml
        df = pd.DataFrame([incoming], columns=["x", "y", "z"])
        df = df.filter(['x', 'y', 'z'])
        if self.debug_predict:
            print(df)
        return df

    def ml_make(self):
        # set a random duration for reading from random line
        ml_read_dur = (random.randrange(3000, 13000) / 1000) * self.glob_speed
        end_time = self.end_time_calc(ml_read_dur)

        # debug
        if self.debug_predict:
            print('C1 ml line read duration = ', ml_read_dur)

        # loop
        while time.time() < end_time:
            # calcs baudrate every cycle
            predict_rate = self.baudrate()

            # passes ml_atom to RNN returns ml_predict from parsing of dataset
            features = config.temp_x_ds, config.temp_y_ds, config.temp_z_ds
            if self.debug_predict:
                print('C2 send to df ', features)

            # make predictions
            df_features = self.make_df(features)
            ml_predict = self.ml_predictions(df_features)
            if self.debug_predict:
                print('C3 ml prediction = ', ml_predict)

            for _ in range(10):
                # parse the result into config
                self.parse_ML_line(ml_predict)
                time.sleep(predict_rate / 10)

            if self.debug_parsing:
                print('C4 config ml ',
                      config.x_ml,
                      config.y_ml,
                      config.z_ml)
            # wait for baudrate to cycle

    # functions producing data
    def ml_predictions(self, features): # RNN predict x, y, z
        # converts incoming tuple into array
        row = array(features)
        if self.debug_predict:
            print('C3 raw row = ', row)

        # reshapes array into 2 dimensions for tf predict
        inputX = reshape(row, (row.shape[0], row.shape[1], 1))

        # makes a prediction
        pred = BODY_model.predict(inputX, verbose=0)
        if self.debug_predict:
            print('C3 raw prediction = ', pred)

        # parses it and returns ias individual vars
        pred_x, pred_y, pred_z = pred[0, 0], pred[0, 1], pred[0, 2]
        if self.debug_predict:
            print('C4 config ml ',
                  pred_x,
                  pred_y,
                  pred_z)

        return (pred_x, pred_y, pred_z)

    def ml_amp_predictions(self, live_amp_in):
        # reshapes array into 2 dimensions for tf predict
        amp_inputX = reshape(live_amp_in, (live_amp_in.shape[0], live_amp_in.shape[1], 1))

        # makes a predictaion
        amp_pred = AMP_model.predict(amp_inputX, verbose=0)

        # parse the result into config
        config.x_ml_live = amp_pred[0, 0]
        config.y_ml_live = amp_pred[0, 1]
        config.z_ml_live = amp_pred[0, 2]

    def parse_ML_line(self, active_line):
        if self.debug_parsing:
            print('parsing line', active_line)
        config.temp_x_ml = (config.x_ml - active_line[0]) / 10
        config.temp_y_ml = (config.y_ml - active_line[1]) / 10
        config.temp_z_ml = (config.z_ml - active_line[2]) / 10
        if self.debug_parsing:
            print('prediction parsing = ', config.temp_x_ml,
                  config.temp_y_ml,
                  config.temp_z_ml
                  )
        config.x_ml = config.temp_x_ml
        config.y_ml = config.temp_y_ml
        config.z_ml = config.temp_z_ml

    def end_time_calc(self, duration):
        # returns the end time for loops
        now_time = time.time()
        return now_time + duration

    def baudrate(self):
        # calculates the baudrate for reading 3-13 seconds
        # (shared by ds read and ml read)
        return (random.randrange(300, 1300) / 1000) * self.glob_speed