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

# audio source variables
my_audio_file = ('data/bill_evans_intro.wav')
audio = AudioSegment.from_wav(my_audio_file)
audio_len = audio.duration_seconds
print (f'length of audio = {audio_len} seconds')

# defines the readable dataset, shuffles it, then resets index
df = pd.read_csv(test_dataset_path, sep=",", header=None, names=["id", "limb", "x", "y", "z", "freq", "amp"])
df = df.filter(['x', 'y', 'z'])
print(df)
index = list(df.index)
index_len = len(index)
shuffle(index)
df = df.iloc[index]
df.reset_index()

# functions producing data
def ml_predictions(features): # RNN predict x, y, z
    row = array(features)
    inputX = reshape(row, (row.shape[0], row.shape[1], 1))
    pred = BODY_model.predict(inputX, verbose=0)
    pred_x, pred_y = pred[0,0], pred [0,1] # only want x and y at this stage
    # print('prediction RNN = ', pred)
    return (pred_x, pred_y)

def what_is_duration(): # of the sound/movment event
    dur_rnd = random() * 2
    return dur_rnd

def choose_incoming_df(): # randomly find a row and use as seed
    ind = randrange(index_len)
    seed = [[df['x'][ind], df['y'][ind], df['z'][ind]]]
    return seed

# A thread that produces data list
def producer_data(out_q):
    while running:
        dur = what_is_duration()
        seed = choose_incoming_df()
        pred_x, pred_y = ml_predictions(seed)

        # Make an (data, event) list and hand it to the consumer
        evt = Event()
        out_q.put((dur, seed, pred_x, pred_y, evt))

        # Wait for the consumer to process the item
        evt.wait()

# functions that consume data
def start_position(dur):
    poss_length = int((audio_len - (dur * 2)) * 1000)
    rnd_length_ms = randrange(poss_length)
    return rnd_length_ms / 1000

def play_sound(start_pos, dur):
    start_pos_ms = start_pos * 1000
    dur_ms = dur * 1000
    end_pos_ms = start_pos_ms + dur_ms
    audio_slice = audio[start_pos_ms : end_pos_ms]
    play(audio_slice)

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

# A thread that consumes data
def consumer(in_q):
    while True:
        # Get some data
        dur, seed, pred_x, pred_y, evt = in_q.get()
        start_pos = start_position(dur)

        # Process the data
        robot_move(pred_x, pred_y)
        play_sound(start_pos, dur) # in seconds!!!

        # Indicate completion
        evt.set()

if __name__ == "__main__":

    #user_dur = input("duration  ? ")
    user_dur = 3 # minutes
    # instantiate the objects
    play_lock = Lock()
    robot = Robot()
    running = True
# todo multiple workers https://pythonprogramming.net/threading-tutorial-python/

    # Create the shared queue and launch both threads
    q = Queue()
    worker_q = Queue()

    now_time = time()
    perf_dur = now_time + user_dur

    # while time() < perf_dur:

    t1 = Thread(target=consumer, args=(q,))
    t2 = Thread(target=consumer, args=(q,))
    t3 = Thread(target=consumer, args=(q,))
    t4 = Thread(target=producer_data, args=(q,))

    t1.start()
    t2.start()
    t3.start()
    t4.start()


    # Wait for all produced items to be consumed
    q.join()
