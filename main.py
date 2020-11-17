import time
import random
import glob
import concurrent.futures
import config
import pyaudio
import numpy as np
from affect import Affect
from ml import Predictions
from robot import Robot
from ui import GUI
from datasetEngine import DataEngine

class Running():
    # conductor for the macro timings for ds read
    def __init__(self, glob_speed, glob_desnity):
        self.affect_interrupt = False
        self.mix_interrupt = False

        # initiate dataset engine
        self.dse = DataEngine(glob_speed)

        # set up ml
        self.pred = Predictions(glob_speed)

        # set up affect and mixing
        self.affect = Affect()


        #
        # # setup robot moving and sounding
        # self.bot = Robot()
        #
        # # setup GUI
        # self.gui = GUI()

    def mlpredictions(self):
        """makes a RNN prediction and parses it"""
        while running:
            self.pred.ml_make()

    def end_time_calc(self, duration):
        # returns the end time for loops
        now_time = time.time()
        return now_time + duration

    def bang_output(self):
        """controls the output streams from raw data generation"""
        while running:

            # calcs rate of smoothing as ms
            bang_rate = (random.randrange(100, 106) * 5 * glob_density) / 1000
            bang_ms = (1 / bang_rate) * 1000

            # stamp current config data as operational robot data

            config.x_ds = config.temp_x_ds
            config.y_ds = config.temp_y_ds
            config.z_ds = config.temp_z_ds
            config.freq_ds = config.temp_freq_ds
            config.amp_ds = config.temp_amp_ds

            config.x_ml = config.temp_x_ml
            config.y_ml = config.temp_y_ml
            config.z_ml = config.temp_z_ml

            time.sleep(bang_ms)

    def robot(self):
        """ get output from smoothing pass to wheels, make a sound"""
        while running:
            for _ in range(random.randrange(6)):
                # calc rate of change random
                data_density = (random.randrange(10, 1300)) * glob_speed # / 1000
                print(f'F data density in ms = {data_density}')

                # move robot and make sound using these configs
                # is instantaious as is sound
                self.bot.robot(data_density)

                print('=================================== playing sound =====================')

                time.sleep(data_density / 1000)

    def affect_listening(self):
        time.sleep(1)
        CHUNK = 2 ** 11
        RATE = 11025
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        random_probability = 0.4

        while running:

            # which amp channel to listen to? 1) live, 2) DS read, 3) random drunk poetry
            amp_channel = random.randrange(3)
            amp_channel_listen_duration = random.randrange(1000, 4000) / 1000
            amp_listen_end_time = time.time() + amp_channel_listen_duration

            while time.time() < amp_listen_end_time:

                # select listening
                if amp_channel == 0:

                    # then listen to the live mic
                    data = np.frombuffer(self.stream.read(CHUNK), dtype=np.int16)
                    # transform the output level to 0 - 100
                    self.peak = (np.average(np.abs(data)) * 2) / 100

                elif amp_channel == 1:
                    # then grab data from config and transform to 0- 100
                    self.peak = config.amp_ds * 100
                    time.sleep(0.02)

                else:
                    # pick a random number
                    self.peak = random.randrange(0, 100)
                    time.sleep(0.02)

                # interrupts processes if medium sound affects (routing matrix only)
                if 40 < self.peak < 80:
                    self.mix_interrupt = True
                    print('##############################    MIX INTERRUPT BANG  ###########################')
                    # hold bang for 0.02 so all waits catch it (which are 0.01!!)
                    time.sleep(0.02)
                    self.mix_interrupt = False

                # interrupts processes if loud sound affects
                # (routing matrix and main dataset file selection (new train of thought))
                elif random.random() > random_probability and self.peak > 81:
                    self.affect_interrupt = True
                    config.affect_interrupt = True
                    print('##############################    AFFECT BANG  ###########################')
                    # hold bang for 0.02 so all waits catch it (which are 0.01!!)
                    time.sleep(0.02)
                    self.affect_interrupt = False
                    config.affect_interrupt = False

        self.snd_listen_terminate()

    def ml_amp(self):
        amp_in = self.peak
        ml_amp_pred = self.pred.ml_amp_predictions(amp_in)

    def snd_listen_terminate(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def affect_mixing(self):
        while running:
            # command a new mix
            self.affect.mixing()

            # control
            self.affect.mix_control(glob_speed)

            # # command a new mix
            # self.affect.mixing()
            #
            # # how long to stay in a mix 1 - 4 seconds
            # rnd_timing = (random.randrange(1000, 4000) / 1000) * glob_speed
            # print('E - affect mixing', rnd_timing, (int(rnd_timing * 100)))
            #
            # # hold mix until affect bang or end of cycle
            # for _ in range(int(rnd_timing) * 100):
            #     # break if loud sound affects flow
            #     if self.affect_interrupt:
            #         time.sleep(0.1)
            #         break
            #     # break if medium sound affects flow
            #     elif self.mix_interrupt:
            #         time.sleep(0.1)
            #         break
            #     time.sleep(0.01)

    # def ui(self):
    #     while running:
    #         self.gui.updater

    def dataset_choice(self):
        while running:
            self.dse.dataset_choice()

    def dataset_read(self):
        while running:
            self.dse.dataset_read()

if __name__ == '__main__':
    glob_density = 1
    glob_speed = 1

    # glob_density = input('what density rate (1 = normal)')
    # glob_speed = input('what global speed (1=normal)')

    # instantiate the baudrate object
    go = Running(glob_speed, glob_density)

    # while the program is running
    while True:
        running = True
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # randomly selects a dataset file to read (6-26 secs)
            p1 = executor.submit(go.dataset_choice)

            # picks a random start point in file and reads (3-13 secs)
            p2 = executor.submit(go.dataset_read)

            # makes ML predictions from p2 input
            p3 = executor.submit(go.mlpredictions)

            # listens to live audio or other streams
            p4 = executor.submit(go.affect_listening)

            #
            # p5 = executor.submit(dse.bang_output)
            # p6 = executor.submit(dse.affect_mixing)
            # p7 = executor.submit(dse.robot)
            # p8 = executor.submit(dse.ml_amp)

            # p9 = executor.submit(dse.gui)
