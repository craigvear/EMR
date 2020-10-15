from keras.models import load_model
from random import shuffle, randrange
import pandas as pd
from numpy import reshape, array
from time import sleep, time
from jetbot import Robot
from threading import Thread, Lock, Event

from pydub import AudioSegment
from pydub.playback import play
import glob
from queue import Queue
from random import random, randrange

# load models from single files
# set up global variables
BODY_model_path = 'training/models/LSTM_Bidirectional_64x4_no_lookback_body_full-dataset_200epochs-3in-3out_model.h5'
BODY_model = load_model(BODY_model_path)
test_dataset_path = 'training/good_dataset_mini.csv'

# audio source variables:
# 2) single audio file
my_audio_file = (data/test.wav)
audio = AudioSegment.from_file(my_audio_file)
audio_len = audio.duration_seconds

# defines the readable dataset, shuffles it, then resets index
running = True

# mix up the original source dataset for reading
df = pd.read_csv(test_dataset_path, sep=",", header=None, names=["id", "limb", "x", "y", "z", "freq", "amp"])
df = df.filter(['x', 'y', 'z'])
print(df)
index = list(df.index)
index_len = len(index)
shuffle(index)
df = df.iloc[index]
df.reset_index()

# functions producing data
def ml_predictions(features):
    row = array(features)
    inputX = reshape(row, (row.shape[0], row.shape[1], 1))
    pred = BODY_model.predict(inputX, verbose=0)
    pred_x, pred_y = pred[0,0], pred [0,1]
    # print('prediction RNN = ', pred)
    return pred_x, pred_y

def what_is_duration():
    dur_rnd = random() * 2
    return dur_rnd

def choose_incoming_df():
    # randomly find a row and use as seed
    ind = randrange(index_len)
    seed = [[df['x'][ind], df['y'][ind], df['z'][ind]]]
    return seed

# A thread that produces data list
def producer_data(out_q):
    while running:
        dur = what_is_duration()
        seed = choose_incoming_df()
        move = ml_predictions(seed)

        # Make an (data, event) list and hand it to the consumer
        evt = Event()
        out_q.put((dur, seed, move, evt))

        # Wait for the consumer to process the item
        evt.wait()

# functions that consume data


# A thread that consumes data
def consumer(in_q):
    while True:
        # Get some data
        dur, seed, move, evt = in_q.get()
        start_pos = start_position()
        # Process the data
        play_sound(start_pos, dur)



        # Indicate completion
        evt.set()

def start_position():


def play_sound(start_pos, dur):
    play_sound = AudioSegment.from_file(song)
    with play_lock:
        play(play_sound)

def threader():
    while True:
        song = q.get()
        play_sound(song)
        q.task_done()



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
    robot.set_motors(left_wheel_move, right_wheel_move)




if __name__ == "__main__":

    # instantiate the objects
    play_lock = Lock()
    robot = Robot()

    # Create the shared queue and launch both threads
    q = Queue()
    t1 = Thread(target=consumer, args=(q,))
    t2 = Thread(target=producer_data, args=(q,))
    t1.start()
    t2.start()

    # Wait for all produced items to be consumed
    q.join()
