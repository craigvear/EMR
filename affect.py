"""
This class listens to the live feed and responds with affect linking.
This changes the mix and sends flags for change
"""

from random import randrange
import config
import time

class Affect():
    def __init__(self):
        print('affect object init')

    def smooth(self):
        """smooths the output frm the mixer"""

        # variables
        # slide time of 20 ms
        slide = 0.02

        # working params
        current_l = config.left_wheel_move_from_smoothing
        target_l = self.left_raw_data_from_affect_mix
        current_r = config.right_wheel_move_from_smoothing
        target_r = self.right_raw_data_from_affect_mix

        # number of intervals
        noi = slide / 10

        # smoothing algo from Max/MSP slide object
        # y(n) = y(n - 1) + ((x(n) - y(n - 1)) / slide)

        # split the delta w/ noi
        increment_value_l = (target_l - current_l) / noi
        increment_value_r = (target_r - current_r) / noi
        print (f'smoothing inc = {increment_value_l}')

        # smooth outputs
        for _ in range(int(noi)):
            current_l += increment_value_l
            current_r += increment_value_r

            # wheel movement = adjusted value
            config.left_wheel_move_from_smoothing = current_l
            config.right_wheel_move_from_smoothing = current_r

            if config.affect_interrupt:
                time.sleep(0.1)
                break

        # print(f'E1 smoothing {current_l},   {current_r}')


        # # define a division rhythm for increments this cycle
        # _factor = randrange(1, 20)
        # division_factor = _factor * randrange(10)
        # print('div factor', division_factor)

    def mixing(self):
        # randomly mixes the data streams to the smoothing/wheels
        left_out = randrange(6)
        if left_out == 0:
            config.left_raw_data_from_affect_mix = config.x_ds
        elif left_out == 1:
            config.left_raw_data_from_affect_mix = config.y_ds
        elif left_out == 2:
            config.left_raw_data_from_affect_mix = config.z_ds
        elif left_out == 3:
            config.left_raw_data_from_affect_mix = config.x_ml
        elif left_out == 4:
            config.left_raw_data_from_affect_mix = config.y_ml
        else:
            config.left_raw_data_from_affect_mix = config.z_ml
        print('Left matrix out is ', left_out)

        right_out = randrange(6)
        if right_out == 0:
            config.right_raw_data_from_affect_mix = config.x_ds
        elif right_out == 1:
            config.right_raw_data_from_affect_mix = config.y_ds
        elif right_out == 2:
            config.right_raw_data_from_affect_mix = config.z_ds
        elif right_out == 3:
            config.right_raw_data_from_affect_mix = config.x_ml
        elif right_out == 4:
            config.right_raw_data_from_affect_mix = config.y_ml
        else:
            config.right_raw_data_from_affect_mix = config.z_ml
        print('Right matrix out is ', right_out)

        # create a pause to avoid multiple bangs
        time.sleep(0.1)