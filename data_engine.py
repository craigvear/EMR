from random import randrange, random
from time import time, sleep
import config
from threading import Thread, Semaphore
from queue import Queue
from keras.models import load_model
import numpy

"""
1. define a loop time 6 - 26 seconds
1a - get a file from mastr dataset

dataset = dir full of individual files
datafile = individual file from dataset
dataitem = individual line from datafile
dataatom = individual piece of data from dataitem"""

# load model from single file
model_path = 'training/models/new_lookback_LSTM-50epochs_full_dataset_512x3_model.h5'
model = load_model(model_path)

def ml_predictions(row):
    # reshape input to be [samples, time steps, features]
    features = row[2:]
    # features = numpy.array(features,dtype = numpy.float)
    print (features)
    inputX = numpy.reshape(features, (1, 1, 5))
    yhat = model.predict(inputX, verbose=0)
    print(yhat)

def dataitem_parser(working_datafile_array, working_dataitem_start):

    row = working_datafile_array.values[working_dataitem_start]
    row = row[:-1]
    ml_predictions(row)
    # convert into dataatoms for rest of code
    # send particuar atom to the dataslider and have the pulse stamp that as global var
    # config.raw_id = row[0]
    # config.raw_limb = row[1]
    # config.raw_x = row[2]
    # config.raw_y = row[3]
    # config.raw_z = row[4]
    # config.raw_freq = row[5]
    # config.raw_amp = row[6]

def read_start_point_from_datafile(working_datafile_array):
    len_working_datafile = len(working_datafile_array)
    print (f'length of working datafile is {len_working_datafile} lines of items')
    rnd_start_point = randrange(len_working_datafile)
    print ('random start point is ', rnd_start_point)
    return rnd_start_point

def is_loop():
    # determines if the parsing is to be looped
    looped = randrange(10)
    if looped > 5: # >= 5 =50% chance of looping
        loop_duration = random() * looped
        print("loop duration = ", loop_duration)
        return loop_duration
    else:
        print ('no loop')
        return 0

