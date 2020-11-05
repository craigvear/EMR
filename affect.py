"""
This class listens to the live feed and responds with affect linking.
This changes the mix and sends flags for change
"""

from random import randrange
import config
from time import sleep

class Affect():
    def __init__(self):
        print('affect object init')

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
        sleep(0.1)