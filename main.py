from threading import Thread, Lock, Event
from queue import Queue
from random import random, randrange
from time import sleep, time
import ML_robot_move

# todo sort threader and queue out in ML-robot_move
# todo move threading to main
# todo create dataset using creative AI computer

play_lock = Lock()

# The threader thread pulls an worker from the queue and processes it
def get_threader():
    while True:
        # gets an worker from the queue
        worker = q_get.get()

        # Run the example job with the avail worker in queue (thread)
        #ML_robot_move.ml_predictions(worker)

        # completed with the job
        q_get.task_done()

def put_threader():
    while True:
        # gets an worker from the queue
        worker = q_put.get()

        # Run the example job with the avail worker in queue (thread)
        ML_robot_move.producer_data(worker)

        # completed with the job
        q_put.task_done()

# Create the queue and threader
q_get = Queue()
q_put = Queue()

# how many threads are we going to allow for
for x in range(10):
     t_get = Thread(target=get_threader)
     t_put = Thread(target=put_threader)

     # classifying as a daemon, so they will die when the main dies
     t_get.daemon = True
     t_put.daemon = True

     # begins, must come after daemon definition
     t_get.start()
     t_put.start()

# 20 jobs assigned.
for worker in range(20):
    q_put.put(worker)
    q_get.put(worker)

# wait until the thread terminates.
q_put.join()
q_get.join()








# from threading import Thread
# from random import randrange, random
# import data_engine as data
# import pandas as pd
# from glob import glob
# from time import sleep, time
# import config
# from random import randrange
# from smoothing import DataAtoms, Data_Smoother
#
# # setup pathway parameters
# # dataset_path = glob('dataset/*')
# dataset_path = 'training/raw_phase1_dataset.csv'
# global_timer = True # todo make this user determined for duration of performance
# # global working_datafile_name
#
# # get list of files from master dataset dir
# raw_files_list = dataset_path
# len_raw_files_list = len(raw_files_list)
#
# print (raw_files_list, len_raw_files_list)
#
#
# """ PLate spinning starts here"""
#
# def timer_dataitems_seq():
#     while global_timer:
#         # loads in the current datafile and converts to dataframe for duration of this function
#         working_datafile_array = pd.read_csv(config.working_datafile_name, sep=",", header=None, names=["id", "limb", "x", "y", "z", "freq", "amp"])
#
#         # random duration of datafile reading 3 -13 secs
#         dataitems_seq_read_dur = randrange(3000, 13000) / 1000
#         start_time_seq_read = time()  # calculates start time for each iteration
#         seq_read_end_time = start_time_seq_read + dataitems_seq_read_dur
#
#         # is it looped
#         is_loop_dur = data.is_loop() # returns with a 0 (no loop) or 0>1 (for loop & duration)
#
#         # get starting point for read seq then
#         # divide into 2 processes: 1 if looped. 2 if not
#         working_dataitem_seq_start = data.read_start_point_from_datafile(working_datafile_array)
#         while time() < seq_read_end_time: # while current time is < duration of reading
#             if is_loop_dur > 0: # calculate current time and while that
#                 loop_out_time = time() + is_loop_dur
#                 loop_working_dataitem_seq_start = working_dataitem_seq_start # create a loop variable so can restart at top of loop
#                 while time() < loop_out_time:  # for each loop iter pass the same start point to the parser
#                     print ('looping ')
#                     data.dataitem_parser(working_datafile_array, loop_working_dataitem_seq_start)
#                     loop_working_dataitem_seq_start += 1
#                     sleep(config.baudrate)  # todo BAUDRATE
#             else:
#                 # working_dataitem_seq_start = data.read_start_point_from_datafile(working_datafile_array) # get new starting poitn
#                 data.dataitem_parser(working_datafile_array, working_dataitem_seq_start)
#                 print ('no loop')
#                 working_dataitem_seq_start += 1
#                 sleep(config.baudrate) # todo BAUDRATE
#
# def baudrate(): # self iterating baudrate for dataset recalls
#     config.baudrate = randrange(300, 1300) / 1000
#     sleep(config.baudrate)
#
# def timer_datafile():
# # master data recall plate spinner = decided which datafile to use from the dataset
#     while global_timer:
#         datafile_dur = randrange(6000, 26000)/1000 # how long to read this file/ master loop?
#         print('how long to read this file = ', datafile_dur)
#
#         rnd_data_list_pos = randrange(len_raw_files_list) # get a random file position from master set
#         print('random file position will be      ', rnd_data_list_pos)
#
#         config.working_datafile_name = raw_files_list[rnd_data_list_pos] # feeds the chosen datafile to the global variable
#         print ('therefore I will be using this file for the moment     ', config.working_datafile_name)
#         sleep(datafile_dur) # todo change this to a while time() < statement to accomodate affect_interrupt_signal
#         #todo affect signal interrupt
#
#
#
#
# if __name__ == "__main__":
#     # smooth_bot = Data_Smoother()
#     # data_atoms_bot = DataAtoms()
#
#     t1 = Thread(target=timer_datafile) # controls the timing for master datafile choice
#     t2 = Thread(target=baudrate)
#     t3 = Thread(target=timer_dataitems_seq)
#     # t4 = Thread(target=data_atom_spinner)
#
#
#     t1.start()
#     t2.start()
#     sleep(0.1)
#     t3.start()
#     # smooth_bot.start()
#     # data_atoms_bot.start()
#
#     t1.join()
#     t2.join()
#     t3.join()
#
#
#
#
#
# # def timer(duration, start):  # manages the global timer for the performance
# #     global running
# #     while running:
# #         now = time()
# #         if start + duration >= now:
# #             running = False
# #             terminate()
# #             return False
# #         else:
# #             sleep(1)
# #
# # def terminate():
# #     data_bot.terminate()
# #
# # def thought_train():  # sets up a thread that harvests new dataset for each random time period (6-26 seconds)
# #     while running:
# #         rnd_dur_train_thought = randrange(6, 26)
# #         data_bot.threader()
# #         sleep(rnd_dur_train_thought)
# #         data_bot.terminate()
# #
# # def wheel_left():
# #     pass
# #
# # def wheel_right():
# #     pass
# #
# # if __name__ == '__main__':
# #
# #     duration = input('duration in mins e.g. 6.5')
# #     duration = int(duration)
# #     start = time()
# #     data_bot = Engine()
# #     # todo a data_bot for each wheel
# #
# #     running = True
# #
# #     t1 = Thread(target=timer, args=(duration, start))
# #     t2 = Thread(target=thought_train, daemon=True)
# #     t3 = Thread(target=wheel_left, daemon=True)
# #     t4 = Thread(target=wheel_right, daemon=True)
# #
# #     t1.start()
# #     t2.start()
# #     t3.start()
# #     t4.start()
# #
# #     t1.join()
# #     t2.join()
# #     t3.join()
# #     t4.join()