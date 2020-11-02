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
        # slide between them at bang_timer ms per step

        while time.time() < end_time:
            # smoothing algo from Max/MSP slide object
            # y(n) = y(n - 1) + ((x(n) - y(n - 1)) / slide)

            current_l = config.left_wheel_move
            target_l = config.left_raw_data
            current_r = config.right_wheel_move
            target_r = config.right_raw_data

            duration = smoothing_dur
            interval = bang_timer

            # number of increments
            noi = duration / interval

            # split the delta w/ noi
            increment_value_l = (target_l - current_l) / noi
            increment_value_r = (target_r - current_r) / noi

            # smooth my ass
            for _ in range(int(noi)):
                current_l += increment_value_l
                current_r += increment_value_r
            print(current_l, current_r)

            config.left_wheel_move = current_l
            config.right_wheel_move = current_r

            # wait for baudrate
            time.sleep(bang_timer)

