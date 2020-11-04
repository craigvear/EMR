"""
This class listens to the live feed and responds with affect linking.
This changes the mix and sends flags for change
"""

from random import randrange
import config

class Affect():
    def __init__(self):
        print('affect object init')

    def mixing(self):
        # randomly mixes the data streams to the smoothing/wheels
        left_out = randrange(6)
        if left_out == 0:
            config.left_raw_data = config.x_ds
        elif left_out == 1:
            config.left_raw_data = config.y_ds
        elif left_out == 2:
            config.left_raw_data = config.z_ds
        elif left_out == 3:
            config.left_raw_data = config.x_ml
        elif left_out == 4:
            config.left_raw_data = config.y_ml
        else:
            config.left_raw_data = config.z_ml
        print('D1 left wheel raw output', config.left_raw_data)

        right_out = randrange(6)
        if right_out == 0:
            config.right_raw_data = config.x_ds
        elif right_out == 1:
            config.right_raw_data = config.y_ds
        elif right_out == 2:
            config.right_raw_data = config.z_ds
        elif right_out == 3:
            config.right_raw_data = config.x_ml
        elif right_out == 4:
            config.right_raw_data = config.y_ml
        else:
            config.right_raw_data = config.z_ml
        print('D2 right wheel raw output', config.right_raw_data)