import time
import random
import glob
import concurrent.futures
import config
import csv
from ml import Predictions
from robot import Robot

# setting up global vars
dataset_list = glob.glob('dataset/*.csv')
running = True
affect_interrupt = False # todo replace with traitlet?

class DatasetEngine():
    # conductor for the macro timings for ds read
    def __init__(self):
        self.affect_interrupt = False

        # select the dataset file for this cycle
        dataset = self.which_dataset()
        print('dataset = ', dataset)

        # send to list making function
        self.dataparsing(dataset)

        # set up ml
        self.ml = Predictions()

        # setup smoothing
        self.bot = Robot()

    def which_dataset(self):
        return random.choice(dataset_list)

    def dataset_choice(self):
        """chooses a dataset file, parses into a list"""

        # if an affect flag happens this will break cycle
        while not self.affect_interrupt:

            # how long to read a dataset file for this cycle
            dataset_choice_dur = (random.randrange(6000, 26000) / 1000)
            print(f'dataset choice duration = {dataset_choice_dur} seconds')

            # select the dataset file for this cycle
            dataset = self.which_dataset()
            print('dataset = ', dataset)

            # send to list making function
            self.dataparsing(dataset)

            # wait for this process to timeout 6-26 seconds
            time.sleep(dataset_choice_dur)

    def dataparsing(self, dataset):
        # takes the chosen dataset file and parses into list
        with open(dataset) as f:
            reader = csv.reader(f)

            # build the dataset as a working list for other threads
            self.data_list = []

            # converts strings into floats
            for row in reader:
                data = [float(item) for item in row[2:]]

                # populate the working list
                self.data_list.append(data)
        print('converted dataset into float list')

    def dataset_read(self):
        """picks a starting line and parses it"""
        # if an affect flag happens this will break cycle
        while not self.affect_interrupt:

            # set a random duration for reading from random line
            dataset_read_dur = (random.randrange(3000, 13000)/ 1000)

            # sorts out durations
            print('dataset line read duration = ', dataset_read_dur)
            end_time = self.end_time_calc(dataset_read_dur)

            # prepare start line to read
            starting_line = self.line_to_read()

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
        ds_len = len(self.data_list)
        if ds_len > 7000:
            ds_len = 7000 # todo sort out the disparity of ds file lengths
        start_line_read = random.randrange(ds_len)

        # print out the details andf returns
        print(f'dataset read start point for reading line {start_line_read}')
        return start_line_read

    def parse(self, parse_end_time, looped, starting_line, baudrate):
        # starting line is
        line_to_read = starting_line
        read_line = self.data_list[line_to_read]
        print(f'reading line {read_line}, parse end time {parse_end_time}, '
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
                    active_line = self.data_list[line_to_read]
                    config.x_ds = active_line[0]
                    config.y_ds = active_line[1]
                    config.z_ds = active_line[2]
                    print('config ds ', config.x_ds, config.y_ds, config.z_ds)
                    line_to_read += 1
                    time.sleep(baudrate)

            else:
                # if no loop
                active_line = self.data_list[line_to_read]
                config.x_ds = active_line[0]
                config.y_ds = active_line[1]
                config.z_ds = active_line[2]
                print('config ds ', config.x_ds, config.y_ds, config.z_ds)
                line_to_read += 1
                time.sleep(baudrate)

    def is_loop(self):
        # determines if the parsing is to be looped
        looped = random.randrange(10)

        # >= 5 =50% chance of looping
        if looped > 5:
            loop_duration = random.randrange(5, 15) / 10
            print("loop duration = ", loop_duration)
            return loop_duration
        else:
            print('no loop')
            return 0

    def mlpredictions(self):
        """makes a RNN prediction and parses it"""
        # if an affect flag happens this will break cycle
        while not self.affect_interrupt:
            # set a random duration for reading from random line
            ml_read_dur = (random.randrange(3000, 13000) / 1000)
            predict_rate = self.baudrate()

            print('ml line read duration = ', ml_read_dur)
            end_time = self.end_time_calc(ml_read_dur)

            while time.time() < end_time:
                # passes ml_atom to RNN returns ml_predict
                features = config.x_ds, config.y_ds, config.z_ds
                print('send to df ', features)
                df_features = self.ml.make_df(features)
                ml_predict = self.ml.ml_predictions(df_features)
                print('ml prediction = ', ml_predict)

                # parse the result into config
                config.x_ml = ml_predict[0]
                config.y_ml = ml_predict[1]
                config.z_ml = ml_predict[2]

                print('config ml ', config.x_ml, config.y_ml, config.z_ml)
                # wait for baudrate to cycle
                time.sleep(predict_rate)

    def mixing(self):
        # TODO affect module proper - this moves to there

        # quick mix TEMPORARY
        left_out = random.randrange(6)
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
        print('left wheel raw output', config.left_raw_data)

        right_out = random.randrange(6)
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
        print('right wheel raw output', config.right_raw_data)

    def end_time_calc(self, duration):
        # returns the end time for loops
        now_time = time.time()
        return now_time + duration

    def roboting(self):
        """smooths output from raw data generation.
        Calcs differences. Moves robot. Makes sound"""
        # if an affect flag happens this will break cycle
        while not self.affect_interrupt:

            # temporary mixing function
            self.mixing()

            # how long we going to smooth at this rate?
            smoothing_dur = random.randrange(150, 1300) / 100

            # endtime calc
            end_time = self.end_time_calc(smoothing_dur)

            # # send the data to smoothing and robot move
            self.bot.smooth(smoothing_dur, end_time)
            print (f'left wheel = {config.left_wheel_move}, right wheel = {config.right_wheel_move}')


if __name__ == '__main__':
    # instantiate the baudrate object
    dse = DatasetEngine()

    # while the program is running
    while running:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            p1 = executor.submit(dse.dataset_choice)
            p2 = executor.submit(dse.dataset_read)
            p3 = executor.submit(dse.mlpredictions)
            # # p4 = executor.submit(dse.affect_mixing)
            p5 = executor.submit(dse.roboting)

