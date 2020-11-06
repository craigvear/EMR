import time
import random
import glob
import concurrent.futures
import config
import csv
import pyaudio
import numpy as np
from affect import Affect
from ml import Predictions
from robot import Robot

# setting up global vars
dataset_list = glob.glob('dataset/*.csv')
running = True

class DatasetEngine():
    # conductor for the macro timings for ds read
    def __init__(self):
        self.affect_interrupt = False
        self.mix_interrupt = False

        # select the init dataset file for this cycle (have something in the pipe
        init_dataset = self.which_dataset()
        # print('A1. init dataset = ', init_dataset)

        # send to list making function
        self.data_list = self.dataparsing(init_dataset)

        # set up ml
        self.ml = Predictions()

        # set up affect and mixing
        self.affect = Affect()

        # setup robot moving and sounding
        self.bot = Robot()

    def which_dataset(self):
        return random.choice(dataset_list)

    def dataset_choice(self):
        """chooses a dataset file, parses into a list"""

        # if an affect flag happens this will break cycle
        while running:

            # select the dataset file for this cycle
            dataset = self.which_dataset()
            print('A2. dataset = ', dataset)

            # send to list making function
            self.data_list = self.dataparsing(dataset)

            # how long to read a dataset file for this cycle
            dataset_choice_dur = (random.randrange(6000, 26000) / 1000)
            print(f'A4 dataset choice duration = {dataset_choice_dur} seconds')

            # wait for this process to timeout 6-26 seconds
            # time.sleep(dataset_choice_dur)
            for _ in range (int(dataset_choice_dur) * 100):
                if self.affect_interrupt:
                    continue
                else:
                    time.sleep(0.01)

    def dataparsing(self, dataset):
        # takes the chosen dataset file and parses into list
        with open(dataset) as f:
            reader = csv.reader(f)

            # reset & build the dataset as a working list for other threads
            data_list = []

            # converts strings into floats
            for row in reader:
                data = [float(item) for item in row[2:]]

                # populate the working list
                data_list.append(data)
        print('A3 converted dataset into float list')
        return data_list

    def dataset_read(self):
        """picks a starting line and parses it"""
        # if an affect flag happens this will break cycle
        while running:
            # grab current data_list and own it locally per cycle
            # to avoid mid-parse changes
            self.local_data_list = self.data_list

            # set a random duration for reading from random line
            dataset_read_dur = (random.randrange(3000, 13000)/ 1000)

            # prepare start line to read
            starting_line = self.line_to_read()

            # sorts out durations
            print('B1 dataset line read duration = ', dataset_read_dur)
            end_time = self.end_time_calc(dataset_read_dur)

            # determine if read is to be looped or sequential
            looped = self.is_loop()

            # calc baudrate
            baudrate = self.baudrate()

            # parse lines of dataset for duration
            self.parse(end_time, looped, starting_line, baudrate)

    def baudrate(self):
        # calculates the baudrate for reading 3-13 seconds
        # (shared by ds read and ml read)
        return (random.randrange(300, 1300) / 1000)

    def line_to_read(self):
        # random line to start reading
        ds_len = len(self.local_data_list)

        start_line_read = random.randrange(ds_len)

        # print out the details andf returns
        print(f'B2 dataset read start point for reading line {start_line_read}')
        return start_line_read

    def parse(self, parse_end_time, looped, starting_line, baudrate):
        # starting line is
        line_to_read = starting_line

        # print out starting line and details
        read_line = self.local_data_list[line_to_read]
        print(f'B3 reading line {read_line}, parse end time {parse_end_time} '
              f'looped {looped}, baudrate {baudrate}')

        # while the read set duration is active
        while time.time() < parse_end_time:
            # if looped
            if looped > 0:
                loop_end = time.time() + looped

                # reset the start read point
                line_to_read = starting_line

                # for each loop
                while time.time() < loop_end:
                    active_line = self.local_data_list[line_to_read]
                    self.parse_active_line(active_line)
                    line_to_read += 1
                    print(f'********  line to read {line_to_read}')
                    time.sleep(baudrate)
            else:
                # if no loop
                active_line = self.local_data_list[line_to_read]
                self.parse_active_line(active_line)
                line_to_read += 1
                print(f'********  line to read {line_to_read}')
                time.sleep(baudrate)

    def parse_active_line(self, active_line):
        config.x_ds = active_line[0]
        config.y_ds = active_line[1]
        config.z_ds = active_line[2]
        print('B4 config ds ', config.x_ds, config.y_ds, config.z_ds)


    def is_loop(self):
        # determines if the parsing is to be looped
        looped = random.randrange(10)

        # >= 5 =50% chance of looping
        if looped > 5:
            loop_duration = random.randrange(5, 15) / 10
            print("B5 loop duration = ", loop_duration)
            return loop_duration
        else:
            print('B5 no loop')
            return 0

    def mlpredictions(self):
        """makes a RNN prediction and parses it"""
        # if an affect flag happens this will break cycle
        while running:
            # set a random duration for reading from random line
            ml_read_dur = (random.randrange(3000, 13000) / 1000)
            predict_rate = self.baudrate()

            # print('C1 ml line read duration = ', ml_read_dur)
            end_time = self.end_time_calc(ml_read_dur)

            while time.time() < end_time:
                # passes ml_atom to RNN returns ml_predict
                features = config.x_ds, config.y_ds, config.z_ds
                print('C2 send to df ', features)
                df_features = self.ml.make_df(features)
                ml_predict = self.ml.ml_predictions(df_features)
                print('C3 ml prediction = ', ml_predict)

                # parse the result into config
                config.x_ml = ml_predict[0]
                config.y_ml = ml_predict[1]
                config.z_ml = ml_predict[2]

                print('C4 config ml ', config.x_ml, config.y_ml, config.z_ml)
                # wait for baudrate to cycle
                time.sleep(predict_rate)

    def end_time_calc(self, duration):
        # returns the end time for loops
        now_time = time.time()
        return now_time + duration

    def roboting(self):
        """smooths output from raw data generation.
        Calcs differences. Moves robot. Makes sound"""
        # if an affect flag happens this will break cycle
        while running:
            # how long we going to smooth at this rate?
            smoothing_dur = random.randrange(150, 1300) / 100

            # endtime calc
            end_time = self.end_time_calc(smoothing_dur)

            # send the data to smoothing and robot move
            self.bot.smooth(smoothing_dur, end_time)

    def affect_listening(self):
        time.sleep(1)
        CHUNK = 2 ** 11
        RATE = 11025
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        random_probability = 0.3

        while running:
            data = np.frombuffer(self.stream.read(CHUNK), dtype=np.int16)
            peak = np.average(np.abs(data)) * 2
            # bars = "#" * int(50 * peak / 2 ** 16)
            # print("%05d %s" % (peak, bars))

            # interrupts processes if medium sound affects (routing matrix only)
            if 6000 < peak < 10000:
                self.mix_interrupt = True
                print('##############################    MIX INTERRUPT BANG  ###########################')
                # hold bang for 0.02 so all waits catch it (which are 0.01!!)
                time.sleep(0.02)
                self.mix_interrupt = False

            # interrupts processes if loud sound affects
            # (routing matrix and main dataset file selection (new train of thought))
            elif random.random() > random_probability and peak > 10001:
                self.affect_interrupt = True
                print('##############################    AFFECT BANG  ###########################')
                # hold bang for 0.02 so all waits catch it (which are 0.01!!)
                time.sleep(0.02)
                self.affect_interrupt = False
                config.affect_interrupt = False

        self.snd_listen_terminate()

    def snd_listen_terminate(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def affect_mixing(self):
        while running:

            # command a new mix
            self.affect.mixing()

            # how long to stay in a mix 1 - 4 seconds
            rnd_timing = (random.randrange(1000, 4000) / 1000)
            print (rnd_timing, (int(rnd_timing * 100)))

            # hold mix until affect bang or end of cycle
            for _ in range(int(rnd_timing) * 100):
                # break if loud sound affects flow
                if self.affect_interrupt:
                    break
                # break if medium sound affects flow
                elif self.mix_interrupt:
                    break
                time.sleep(0.01)

if __name__ == '__main__':
    # instantiate the baudrate object
    dse = DatasetEngine()

    # while the program is running
    while True:
        running = True
        with concurrent.futures.ThreadPoolExecutor() as executor:
            p1 = executor.submit(dse.dataset_choice)
            p2 = executor.submit(dse.dataset_read)
            p3 = executor.submit(dse.mlpredictions)
            p4 = executor.submit(dse.affect_listening)
            p5 = executor.submit(dse.affect_mixing)
            p6 = executor.submit(dse.roboting)
