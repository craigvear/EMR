import time
import random
import concurrent.futures
import config
import csv
from ml import Predictions
from smoothing import Smoother

class DatasetEngine():
    # conducts the whole macro timings
    def __init__(self):
        pass

    def dataset_choice(self):
        """chooses a dataset file, parses into a list"""

        # if an affect flag happens this will break cycle
        while not self.affect_interrupt:

            # how long to read a dataset file
            dataset_choice_dur = (random.randrange(6000, 26000) / 1000)
            print(f'dataset choice duration = {dataset_choice_dur} seconds')

            # todo choose a dataset file and send to config file
            dataset = test_dataset_path
            print('dataset = ', config.dataset)

            # send to list making function
            self.dataparsing(dataset)

            # wait for this process to timeout 6-26 seconds
            time.sleep(dataset_choice_dur)

            return 'done'

    def dataparsing(self, dataset):
        # takes the chosen dataset file and parses into list
        with open(dataset) as f:
            reader = csv.reader(f)
            self.data_list = []
            # converts strings into floats
            for row in reader:
                data = [float(item) for item in row[2:]]
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

            print('done')

    def baudrate(self):
        # calculates the daudrate for reading 3-13 seconds
        return (random.randrange(300, 1300) / 1000)

    def line_to_read(self):
        # random line to start reading
        ds_len = len(self.data_list)
        start_line_read = random.randrange(ds_len)

        # print out the details andf returns
        print(f'dataset read start point for reading line {start_line_read}')
        return start_line_read

    def parse(self, end_time, looped, starting_line, baudrate):
        # starting line is
        line_to_read = starting_line
        read_line = self.data_list[line_to_read]
        print('reading line ', read_line)

        # while the read set duration is active
        while time.time() < end_time:
            # if looped
            if looped > 0:
                loop_end = time.time() + looped

                # reset the start read point
                line_to_read = starting_line

                # for each loop
                while time.time() < loop_end:
                    active_line = self.data_list[line_to_read]
                    print('output line of ds = ', active_line)
                    config.x_ds, config.y_ds, config.z_ds = active_line[:3]
                    line_to_read += 1
                    time.sleep(baudrate)

            else:
                # if no loop
                active_line = self.data_list[line_to_read]
                print('output line of ds = ', active_line)
                config.x_ds, config.y_ds, config.z_ds = active_line[:3]
                line_to_read += 1
                time.sleep(baudrate)

    def is_loop(self):
        # determines if the parsing is to be looped
        looped = random.randrange(10)

        # >= 5 =50% chance of looping
        if looped > 5:
            loop_duration = random.random() * 2
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
                ml_predict = self.ml.ml_predictions(self.ml_atom)
                print('ml prediction = ', ml_predict)

                # parse the result into config
                config.x_ml, config.y_ml, config.z_ml = ml_predict

                # wait for baudrate to cycle
                time.sleep(predict_rate)

        print('done')

    def mixing(self):
        # TODO affect module proper

        # quick mix TEMPORARY
        left_out = random.randrange(6)
        if left_out == 0:
            config.left_raw_data = config.x_ds
        elif left_out == 1:
            config.left_raw_data = config.y_ds
        elif left_out == 1:
            config.left_raw_data = config.z_ds
        elif left_out == 1:
            config.left_raw_data = config.x_ml
        elif left_out == 1:
            config.left_raw_data = config.y_ml
        else:
            config.left_raw_data = config.z_ml

        right_out = random.randrange(6)
        if right_out == 0:
            config.right_raw_data = config.x_ds
        elif right_out == 1:
            config.right_raw_data = config.y_ds
        elif right_out == 1:
            config.right_raw_data = config.z_ds
        elif right_out == 1:
            config.right_raw_data = config.x_ml
        elif right_out == 1:
            config.right_raw_data = config.y_ml
        else:
            config.right_raw_data = config.z_ml

    def end_time_calc(self, duration):
        # returns the end time for loops
        now_time = time.time()
        return now_time + duration

    def smoothing(self):
        # temporary mixing function
        self.mixing()

        # hoe long we going to smooth at this rate?
        smoothing_dur = random.randrange(150, 1300) / 1000

        # endtime calc
        end_time = self.end_time_calc(smoothing_dur)

        # units of smoothing
        bang_timer = 0.03

        self.left_wheel, self.right_wheel = \
            self.smoother.smooth(smoothing_dur,bang_timer, end_time)

        print (f'left wheel = {self.left_wheel}, right wheel = {self.right_wheel}')

        print('done')


if __name__ == '__main__':

    test_dataset_path = 'training/raw_phase1_dataset.csv'

    running = True
    affect_interrupt = False
    # instantiate the baudrate object
    dse = DatasetEngine()

    affect_interrupt = False
    # todo choose a dataset file and send to config file
    dataset = test_dataset_path
    print('dataset = ', dataset)

    # send to list making function
    dataparsing(dataset)

    # set up ml
    ml = Predictions()
    ml_atom = self.ml.seed(self.data_list)

    # setup smoothing
    smoother = Smoother()


    # dse.dataset_choice()
    # dse.dataset_read()
    # dse.smoothing()

    # # while the program is running
    while running:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            p1 = executor.submit(dse.dataset_choice)
            # p2 = executor.submit(dse.dataset_read)
            # p3 = executor.submit(dse.mlpredictions)
            # p4 = executor.submit(dse.affect_mixing)
            # p5 = executor.submit(dse.smoothing)
            # p6 = executor.submit(dse.move_robot)

