from random import randrange, random
from time import time, sleep
import config
from threading import Thread, Semaphore
from queue import Queue
from keras.models import load_model
import numpy

from time import sleep, time
# from jetbot import Robot
from threading import Thread, Lock, Event

from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play
import glob
from queue import Queue





class Robot():
    def __init__(self):


    def move(self):
        # robot.set_motors(config.left_wheel_move, config.right_wheel_move)
        self.sound()

    def sound(self):
        pass



# # A thread that produces data list
# def producer_data():
#     dur = what_is_duration()
#     seed = choose_incoming_df()

    # # get predictions. x & y for wheel movement, z for duration variability
    # pred_x, pred_y, pred_z = ml_predictions(seed)
    # return (dur, pred_x, pred_y, pred_z)


# def what_is_duration(): # of the sound/movment event
#     dur_rnd = random()
#     rnd_div = randrange(20)
#     return (dur_rnd / (rnd_div + 1)) + 0.03


# thread that consumes data
def consumer(incoming_data):
    # Get some data
    ((packed_data, evt)) = incoming_data
    (dur, pred_x, pred_y, pred_z) = data
    start_pos = start_position(dur, pred_z)

    with play_lock:
        # Process the data
        play_sound(start_pos, dur)  # in seconds!!!
        robot_move(pred_x, pred_y)

    # indicate completion
    evt.set()

def start_position(dur, pred_z):
    poss_length = int((audio_len - (dur)) * 1000)
    rnd_length_ms = randrange(poss_length) * pred_z
    return rnd_length_ms / 1000

def play_sound(start_pos, dur):
    start_pos_ms = start_pos * 1000
    dur_ms = dur * 1000
    end_pos_ms = start_pos_ms + dur_ms
    audio_slice = audio[start_pos_ms: end_pos_ms]

    play(audio_slice)
    sleep(dur-0.02)

def robot_move(pred_x, pred_y):
    multi_factor = 1
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
    # robot.set_motors(left_wheel_move, right_wheel_move)


def threader():
    while True:
        # gets an worker from the queue
        data = q.get()

        # Run the example job with the avail worker in queue (thread)
        consumer(data)

        # completed with the job
        q.task_done()

if __name__ == "__main__":
    # get the length of the improv
    length = input('What length?   (in whole minutes e.g. 2) ___ ')
    time_now = time()
    end_time = time_now + (int(length) * 60)

    # instantiate the objects
    play_lock = Lock()
    # robot = Robot()

    # Create the shared queue and launch both threads
    q = Queue()

    # how many threads are we going to allow for
    for x in range(3):
        t1 = Thread(target=threader)

        # classifying as a daemon, so they will die when the main dies
        t1.daemon = True

        # begins, must come after daemon definition
        t1.start()

    # 10 jobs assigned.
    while time() < end_time:
        for worker in range(3):
            evt = Event()
            # produce some data
            data = producer_data()

            # Make a data, evt pair and hand to q for customer
            q.put((data, evt))

            # wait for cusotmer to process
            evt.wait()

    # wait until the thread terminates.
    q.join()






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

# def read_start_point_from_datafile(working_datafile_array):
#     len_working_datafile = len(working_datafile_array)
#     print (f'length of working datafile is {len_working_datafile} lines of items')
#     rnd_start_point = randrange(len_working_datafile)
#     print ('random start point is ', rnd_start_point)
#     return rnd_start_point

# def is_loop():
#     # determines if the parsing is to be looped
#     looped = randrange(10)
#     if looped > 5: # >= 5 =50% chance of looping
#         loop_duration = random() * looped
#         print("loop duration = ", loop_duration)
#         return loop_duration
#     else:
#         print ('no loop')
#         return 0

