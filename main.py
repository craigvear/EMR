import time
import random
import concurrent.futures
import pyaudio
import numpy as np
import config
from affect import Affect
from ml import Predictions
from robot import Robot
from ui import GUI
from datasetEngine import DataEngine

# todo: sort out deviation and smoothing at robot end
# todo: GUI
# todo: tf2 conflict on JetBot
# todo: wheel independence

class Running():
    # debug toggles
    debug_report = False
    debug_robot = False

    # conductor for the macro timings for ds read
    def __init__(self, glob_speed, glob_density):
        # self.affect_interrupt = False
        # self.mix_interrupt = False
        self.glob_speed = glob_speed
        self.glob_density = glob_density

        # initiate dataset engine
        self.dse = DataEngine(self.glob_speed)

        # set up ml
        self.pred = Predictions(self.glob_speed)

        # set up affect and mixing
        self.affect = Affect(self.glob_speed)

        # setup robot 4 moving and sounding
        self.bot = Robot(self.glob_density)

        # # setup GUI
        # self.gui = GUI()

    def mlpredictions(self):
        """makes a RNN prediction and parses it"""
        while running:
            self.pred.ml_make()

    # def end_time_calc(self, duration):
    #     # returns the end time for loops
    #     now_time = time.time()
    #     return now_time + duration

    def bang_output(self):
        """controls the output streams from raw data generation"""
        while running:
            # calcs rate of sounding as ms
            bang_rate = (random.randrange(150, 300) * glob_density) / 1000
            # bang_secs = (1 / bang_rate)
            if self.debug_report:
                print ('bang outputs wait = ', bang_rate)
            # stamp current config data as operational robot data
            self.affect.bang_mix_out()

            # config.x_ds = config.temp_x_ds
            # config.y_ds = config.temp_y_ds
            # config.z_ds = config.temp_z_ds
            # config.freq_ds = config.temp_freq_ds
            # config.amp_ds = config.temp_amp_ds
            #
            # config.x_ml = config.temp_x_ml
            # config.y_ml = config.temp_y_ml
            # config.z_ml = config.temp_z_ml

            time.sleep(bang_rate)

    def robot(self):
        """ get output from smoothing pass to wheels, make a sound"""
        while running:
            for _ in range(random.randrange(6)):
                # calc rate of change random
                self.data_density = (random.randrange(20, 300)) * glob_density # / 1000
                if self.debug_robot:
                    print(f'F data density in ms = {self.data_density}')

                # move robot and make sound using these configs
                # is instantaious as is sound

                self.bot.robot_control(self.data_density)

                if self.debug_robot:
                    print(f'=================================== playing sound =====================')

                time.sleep(self.data_density / 1000)

    # def robot_right(self):
    #     """ get output from smoothing pass to wheels, make a sound"""
    #     self.wheel = 'right'
    #     while running:
    #         for _ in range(random.randrange(6)):
    #             # calc rate of change random
    #             self.data_density = (random.randrange(20, 300)) * glob_density # / 1000
    #             if self.debug_robot:
    #                 print(f'F data density in ms = {self.data_density}')
    #
    #             # move robot and make sound using these configs
    #             # is instantaious as is sound
    #             self.bot_right.robot_control(self.data_density)
    #
    #             # else:
    #             #     self.bot_right.robot(data_density, wheel)
    #
    #             if self.debug_robot:
    #                 print('=================================== playing sound  {self.wheel}  =====================')
    #
    #             time.sleep(self.data_density / 1000)

    def affect_listening(self):
        """leave this as a standalone func to control sample time integrity"""
        # time.sleep(1)
        CHUNK = 2 ** 11
        RATE = 44100
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

        while running:
            data = np.frombuffer(self.stream.read(CHUNK), dtype=np.int16)
            # transform the output level to 0 - 100
            self.peak = (np.average(np.abs(data)) * 2) / 100
            if self.debug_report:
                print(f' peak level from live mic = {self.peak}')

        # self.affect.snd_listen_terminate()

    def choose_listening(self):
        random_probability = 0.4

        while running:
            # which amp channel to listen to? 1) live, 2) DS read, 3) random drunk poetry
            amp_channel = random.randrange(3)
            amp_channel_listen_duration = random.randrange(1000, 4000) / 1000
            amp_listen_end_time = time.time() + amp_channel_listen_duration
            if self.debug_report:
                print(f'listening to {amp_channel}, duration {amp_channel_listen_duration}')

            while time.time() < amp_listen_end_time:

                # select listening
                if amp_channel == 0:

                    listen_label = 'live mic'
                    # then listen to the live mic
                    active_peak = self.peak

                    # data = np.frombuffer(self.stream.read(CHUNK), dtype=np.int16)
                    # # transform the output level to 0 - 100
                    # self.peak = (np.average(np.abs(data)) * 2) / 100

                elif amp_channel == 1:
                    listen_label = 'DS amp reading'

                    # then grab data from config and transform to 0- 100
                    active_peak = config.amp_ds
                    time.sleep(0.02)

                else:
                    listen_label = 'random'
                    # pick a random number
                    active_peak = random.randrange(0, 300)
                    time.sleep(0.02)

                # interrupts processes if medium sound affects (routing matrix only)
                if 100 < active_peak < 200:
                    config.mix_interrupt = True
                    if self.debug_report:
                        print(f'##############################    MIX INTERRUPT BANG  {listen_label}, {active_peak}  ###########################')
                    # hold bang for 0.02 so all waits catch it (which are 0.01!!)
                    time.sleep(0.02)
                    config.mix_interrupt = False

                # interrupts processes if loud sound affects
                # (routing matrix and main dataset file selection (new train of thought))
                elif random.random() > random_probability and active_peak > 201:
                    config.affect_interrupt = True
                    if self.debug_report:
                        print(f'##############################    AFFECT BANG  {listen_label}, {active_peak} ###########################')
                    # hold bang for 0.02 so all waits catch it (which are 0.01!!)
                    time.sleep(0.02)
                    config.affect_interrupt = False

    # todo - abandoned for now as input shapes are wrong
    def ml_amp(self):
        while running:
            amp_in = self.peak / 300
            ml_amp_pred = self.pred.ml_amp_predictions(amp_in)
            print('ml amp prediction = ', ml_amp_pred)

            # calculates the baudrate for reading 3-13 seconds
            time.sleep((random.randrange(300, 1300) / 1000) * self.glob_speed)

    def affect_mixing(self):
        while running:
            # command a new mix
            self.affect.mixing()

            # control
            self.affect.mix_control()

    # todo - UI abandoned for now
    def ui(self):
        while running:
            self.gui.updater()

    def dataset_choice(self):
        while running:
            self.dse.dataset_choice()

    def dataset_read(self):
        while running:
            self.dse.dataset_read()

if __name__ == '__main__':
    glob_density = random.randrange(200, 2000) / 1000
    glob_speed = random.randrange(200, 2000) / 1000
    running = True

    # instantiate the baudrate object
    go = Running(glob_speed, glob_density)

    # go.robot('left')

    # while the program is running
    while running:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # randomly selects a dataset file to read (6-26 secs)
            p1 = executor.submit(go.dataset_choice)

            # picks a random start point in file and reads (3-13 secs)
            p2 = executor.submit(go.dataset_read)

            # makes ML predictions from p2 input
            p3 = executor.submit(go.mlpredictions)

            # listens to live audio
            p4 = executor.submit(go.affect_listening)

            # chooses which listening
            p5 = executor.submit(go.choose_listening)

            # bangs the mix output to the robot
            p6 = executor.submit(go.bang_output)

            # bangs and mixes outputs to the robot class
            p7 = executor.submit(go.affect_mixing)

            # controls the robot class LEFT wheel
            p8 = executor.submit(go.robot)

            # todo - abandoned for now as input shapes are wrong
            # generates an xyz response from NN using live mic
            # p9 = executor.submit(go.ml_amp)

            # # controls UI
            # p10 = executor.submit(go.ui)
