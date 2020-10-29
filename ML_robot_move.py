# thanks to # todo multiple workers https://pythonprogramming.net/threading-tutorial-python/
from keras.models import load_model
from random import shuffle, randrange
import pandas as pd
from numpy import reshape, array
from time import sleep, time
# from jetbot import Robot
from threading import Thread, Lock, Event

from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play
import glob
from queue import Queue
from random import random, randrange

# load models from single files
# set up global variables
BODY_model_path = 'training/models/LSTM_Bidirectional_64x4_no_lookback_body_full-dataset_200epochs-3in-3out_model.h5'
BODY_model = load_model(BODY_model_path)
test_dataset_path = 'training/good_dataset_mini.csv'

# audio source variables
audio_file = ('data/bill_evans_intro.wav')
audio = AudioSegment.from_wav(audio_file)
audio_len = audio.duration_seconds



# defines the readable dataset, shuffles it, then resets index
df = pd.read_csv(test_dataset_path, sep=",", header=None, names=["id", "limb", "x", "y", "z", "freq", "amp"])
df = df.filter(['x', 'y', 'z'])
print(df)
index = list(df.index)
index_len = len(index)
shuffle(index)
df = df.iloc[index]
df.reset_index()

# A thread that produces data list
def producer_data():
    dur = what_is_duration()
    seed = choose_incoming_df()
    pred_x, pred_y = ml_predictions(seed)

    # Make an (data, event) list and hand it to the consumer
    # evt = Event()
    return (dur, pred_x, pred_y)

# functions producing data
def ml_predictions(features): # RNN predict x, y, z
    row = array(features)
    inputX = reshape(row, (row.shape[0], row.shape[1], 1))
    pred = BODY_model.predict(inputX, verbose=0)
    pred_x, pred_y = pred[0,0], pred [0,1] # only want x and y at this stage
    # print('prediction RNN = ', pred)
    return pred_x, pred_y

def what_is_duration(): # of the sound/movment event
    dur_rnd = random() * 2
    return dur_rnd

def choose_incoming_df(): # randomly find a row and use as seed
    ind = randrange(index_len)
    seed = [[df['x'][ind], df['y'][ind], df['z'][ind]]]
    return seed

# thread that consumes data
def consumer(data):
    # Get some data
    (dur, pred_x, pred_y) = data
    start_pos = start_position(dur)

    with play_lock:
        # Process the data
        play_sound(start_pos, dur)  # in seconds!!!
        robot_move(pred_x, pred_y)

def start_position(dur):
    poss_length = int((audio_len - (dur * 2)) * 1000)
    rnd_length_ms = randrange(poss_length)
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

    # instantiate the objects
    play_lock = Lock()
    # robot = Robot()

    # Create the shared queue and launch both threads
    q = Queue()

    # how many threads are we going to allow for
    for x in range(10):
        t1 = Thread(target=threader)

        # classifying as a daemon, so they will die when the main dies
        t1.daemon = True

        # begins, must come after daemon definition
        t1.start()

    # 10 jobs assigned.
    while True:
        for worker in range(10):
            data = producer_data()
            q.put(data)
            print (worker)

    # wait until the thread terminates.
    q.join()
