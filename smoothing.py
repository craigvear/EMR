import time
import config
from random import randrange

"""
takes the stored variables in config, and mixes then then smooths output
"""
class Smoother(): # smooths the data as a thread class
    def __init__(self):
        print("Smoothing, baby")

    def smooth(self, smoothing_dur, bang_timer, end_time):
        # increments
        num_increments = int(smoothing_dur/bang_timer)

        # current wheel value
        current_value_left = config.left_wheel_move
        current_value_right = config.right_wheel_move

        # new mixed value
        new_value_left = config.left_raw_data
        new_value_right = config.right_raw_data

        # differnce
        inc_delta_left = (current_value_left - new_value_left) / num_increments
        inc_delta_right = (current_value_right - new_value_right) / num_increments

        # slide between them at 10 ms per step
        while time.time() < end_time:
            current_value_left += inc_delta_left
            current_value_right += inc_delta_right
            print(current_value_left, current_value_right)
            time.sleep(bang_timer)

        return config.left_wheel_move, config.right_wheel_move
