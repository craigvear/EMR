import time
import config

from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play
from random import randrange

"""
takes the stored variables in config, and mixes then then smooths output
"""
# class Robot(): # smooths the data as a thread class
#     def __init__(self):
# audio source variables
audio_file = 'data/jarrett_snippet.wav'
audio = AudioSegment.from_wav(audio_file)
audio_len = audio.duration_seconds
print("Roboting, baby")

interval = 0.1

poss_length = int(audio_len - (interval))
start_pos_ms = randrange(poss_length * 1000)
dur_ms = interval * 1000
end_pos_ms = start_pos_ms + dur_ms

print (poss_length, start_pos_ms, end_pos_ms)

audio_slice = audio[start_pos_ms: end_pos_ms]

print ('2')

play(audio_slice)
time.sleep(interval - 0.02)


# # config.left_wheel_move = current value
# # config.left_raw_data = target
# # result [y(n)] = y(n - 1) + ((x(n) - y(n - 1)) / slide)
# # current value will then = result
# # config.left_wheel_move = current value
#
#
# current = 1.2
# target = 4
# target2 = 1
# duration = 3
# interval = 0.1
#
# # number of increments
# noi = duration / interval
# # print(noi)
#
# # split the delta w/ noi
# increment_value = (target - current) / noi
# # print(increment_value)
#
# print(current)
#
# for _ in range(int(noi)):
#     # current
#     current += increment_value
# print(current)
#
# # split the delta w/ noi
# increment_value = (target2 - current) / noi
# # print(increment_value)
#
# for _ in range(int(noi)):
#     # current
#     current += increment_value
# print(current)
#
#
#
#
# # import config
# # import random
# #
# # ml_out_4_mixer = random.randrange(6)
# # if ml_out_4_mixer == 0:
# #     left_raw = config.x_ml
# #
# #
# # print(ml_out_4_mixer)
# #
#
#
# # import csv
# # import random
# # import time
# #
# #
# # dataset = 'training/raw_phase1_dataset.csv'
# #
# # dataset_read_dur = random.randrange(3000, 13000)
# # start_time = time.time()
# # end_time = start_time + (dataset_read_dur/1000)
# #
# # # convert current dataset into tuples
# # with open(dataset) as f:
# #     reader = csv.reader(f)
# #     your_list = list(reader)
# #
# # # print(len(your_list))
# #
# # my_num = (your_list[3][3])
# #
# # print(float(my_num))
# #
# # # print(dataset_read_dur/1000)
# # # time.sleep(dataset_read_dur / 1000)