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
        # intiates object variables
        self.right_raw_data_from_affect_mix = 0
        self.left_raw_data_from_affect_mix = 0

    def smooth(self):
        """smooths the output from the mixer"""
        # grabs current wheel settings from config
        current_l = config.left_wheel_move_from_smoothing
        current_r = config.right_wheel_move_from_smoothing

        # grabs output from mixer
        target_r = config.right_raw_data_from_affect_mix
        target_l = config.left_raw_data_from_affect_mix

        # number of intervals
        # noi = slide / 10

        # smoothing algo from Max/MSP slide object
        # y(n) = y(n - 1) + ((x(n) - y(n - 1)) / slide)

        # split the delta
        increment_value_l = (target_l - current_l) / 20
        increment_value_r = (target_r - current_r) / 20
        # print (f' inc = {increment_value_l}')

        # output result back out to config
        config.left_wheel_move_from_smoothing = current_l + increment_value_l
        config.right_wheel_move_from_smoothing = current_r + increment_value_r


    def mixing(self):
        # randomly mixes the data streams to the smoothing/wheels
        left_out = randrange(9)
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
        elif left_out == 5:
            config.left_raw_data_from_affect_mix = config.z_ds
        elif left_out == 6:
            config.left_raw_data_from_affect_mix = config.x_ml_live
        elif left_out == 7:
            config.left_raw_data_from_affect_mix = config.y_ml_live
        else:
            config.left_raw_data_from_affect_mix = config.z_ml_live
        print('Left matrix out is ', left_out)

        right_out = randrange(9)
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
        elif left_out == 5:
            config.right_raw_data_from_affect_mix = config.z_ds
        elif left_out == 6:
            config.right_raw_data_from_affect_mix = config.x_ml_live
        elif left_out == 7:
            config.right_raw_data_from_affect_mix = config.y_ml_live
        else:
            config.right_raw_data_from_affect_mix = config.z_ml_live
        print('Right matrix out is ', right_out)

        # # create a pause to avoid multiple bangs
        # time.sleep(0.1)


if __name__ == '__main__':

    bot = Affect()

    while True:
        config.left_raw_data_from_affect_mix = randrange(-100, 100)/ 100
        config.right_raw_data_from_affect_mix = randrange(-100, 100)/ 100

        print('random  are ', config.left_raw_data_from_affect_mix, config.right_raw_data_from_affect_mix)
        bot.smooth()

        print('configs are ', config.left_wheel_move_from_smoothing, config.right_wheel_move_from_smoothing)
        time.sleep(1)
