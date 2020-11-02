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
        inc_delta_left = (new_value_left - current_value_left) / num_increments
        inc_delta_right = (new_value_right - current_value_right) / num_increments

        # slide between them at 10 ms per step
        while time.time() < end_time:
            current_value_left += inc_delta_left
            current_value_right += inc_delta_right
            print(current_value_left, current_value_right)
            time.sleep(bang_timer)

        return config.left_wheel_move, config.right_wheel_move


    # def run(self):
    #     while self.running:
    #         self.ramp_rate = config.baudrate #/ 1000  # what is current baudrate - which might change with instances of class
    #         print ('ramprate is = ', self.ramp_rate)
    #         self.calc_x() # calculate starting parameters
    #         # self.old_x = config.raw_x # logs the raw_x(n-1) ready for next smoothing
    #         # todo all others .calc
    #
    #         # define time steps
    #         timer = time() # now time
    #         end_time = timer + self.ramp_rate # end time
    #
    #         while time() < end_time: # for duration of loop
    #             self.smooth_x() # activate a single step of smoothing, pass increment value from calc
    #             # todo all other vars
    #             sleep(0.01)
    #         self.old_x = self.target_x

    # def calc_x(self): # calculate parameters per loop
    #     self.target_x = config.raw_x  # current target value of raw_x(n)
    #     config.temp_x = self.old_x
    #     print (f'paras:, target x {self.target_x}, odl x {self.old_x}, ramp rate * 1000 = {self.ramp_rate * 1000}')
    #     self.increment_x = ((self.target_x - self.old_x) / (self.ramp_rate * 1000))  # what is the step increment
    #     print ('increment = ', self.increment_x)
    #
    # def smooth_x(self): # calculate 1 step of smoothing and updates config param
    #     config.temp_x += self.increment_x
    #     print(config.temp_x)


    # """these deal with banging out the usable data atoms for movement"""
    # def mixer(self):
    #     while self.running:
    #         bang_rate = randrange(150, 1300) / 1000 # in ms
    #         config.atom_x = config.temp_x # round to 2dp and save as atom_x
    #         print ('atoms = ', config.atom_x)
    #         print('bang rate ', bang_rate)
    #         # todo all others y, z, freq, amp
    #         sleep(bang_rate)
