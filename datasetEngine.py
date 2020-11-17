import config
import random
import time
import glob
import csv

class DataEngine():
    # setting up global vars
    dataset_list = glob.glob('dataset/*.csv')

    # debug toggles
    debug_choose = False
    debug_read = False

    def __init__(self, glob_speed):
        print('dataset engine is GOOOO')
        self.glob_speed = glob_speed

        # select the init dataset file for this cycle (have something in the pipe
        init_dataset = self.which_dataset()
        # print('A1. init dataset = ', init_dataset)

        # send to list making function
        self.data_list = self.dataparsing(init_dataset)

    def which_dataset(self):
        return random.choice(self.dataset_list)

    def dataset_choice(self):
        """chooses a dataset file, parses into a list"""
        # while running:

        # select the dataset file for this cycle
        dataset = self.which_dataset()
        # print('A2. dataset = ', dataset)

        # send to list making function
        self.data_list = self.dataparsing(dataset)

        # how long to read a dataset file for this cycle
        dataset_choice_dur = (random.randrange(6000, 26000) / 1000) * self.glob_speed
        if self.debug_choose:
            print(f'A4 dataset choice duration = {dataset_choice_dur} seconds')

        # wait for this process to timeout 6-26 seconds
        # time.sleep(dataset_choice_dur)
        for _ in range (int(dataset_choice_dur) * 100):
            if config.affect_interrupt:
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
        if self.debug_choose:
            print('A3 converted dataset into float list')
        return data_list

    def dataset_read(self):
        """picks a starting line and parses it"""
        # while self.running:
        # grab current data_list and own it locally per cycle
        # to avoid mid-parse changes
        self.local_data_list = self.data_list

        # set a random duration for reading from random line
        # before choosing another from current set
        dataset_read_dur = (random.randrange(3000, 13000) / 1000) * self.glob_speed

        # prepare start line to read
        starting_line = self.line_to_read()

        # sorts out durations
        if self.debug_choose:
            print('B1 dataset line read duration = ', dataset_read_dur)
        end_time = self.end_time_calc(dataset_read_dur)

        # determine if read is to be looped or sequential
        looped = self.is_loop()

        while time.time() < end_time:
            # calc baudrate and cycle clock for speed of line read
            baudrate = self.baudrate()

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
                    if self.debug_read:
                        print(f'********  line to read LOOPING {line_to_read}')
                    # print(f'config data = {config.x_ds}, {config.y_ds}, {config.z_ds}')

                    # pause for 10th of baudrate, while parse_active_line slides
                    time.sleep(baudrate/10)
            else:
                # if no loop
                active_line = self.local_data_list[starting_line]
                self.parse_active_line(active_line)
                starting_line += 1
                if self.debug_read:
                    print(f'********  line to read NO LOOP {starting_line}')
                # print(f'config data = {config.x_ds}, {config.y_ds}, {config.z_ds}')

                # pause for 10th of baudrate, while parse_active_line slides
                time.sleep(baudrate/10)

    def baudrate(self):
        # calculates the baudrate for reading 3-13 seconds
        # (shared by ds read and ml read)
        return (random.randrange(300, 1300) / 1000) * self.glob_speed

    def line_to_read(self):
        # random line to start reading
        ds_len = len(self.local_data_list)

        start_line_read = random.randrange(ds_len)

        # print out the details andf returns
        if self.debug_read:
            print(f'B2 dataset read start point for reading line {start_line_read}')
        return start_line_read

    def parse_active_line(self, active_line):
        config.temp_x_ds = (config.x_ds - active_line[0]) / 10
        config.temp_y_ds = (config.y_ds - active_line[1]) / 10
        config.temp_z_ds = (config.z_ds - active_line[2]) / 10
        config.temp_freq_ds = (config.freq_ds - active_line[3]) / 10
        config.temp_amp_ds = (config.amp_ds - active_line[4]) / 10

        # config.x_ds = temp_x_ds
        # config.y_ds = temp_y_ds
        # config.z_ds = temp_z_ds
        # config.freq_ds = temp_freq_ds
        # config.amp_ds = temp_amp_ds
        if self.debug_read:
            print('B4 config.temp ds ', config.temp_x_ds,
                  config.temp_y_ds,
                  config.temp_z_ds)

    def is_loop(self):
        # determines if the parsing is to be looped
        looped = random.randrange(10)

        # >= 5 =50% chance of looping
        if looped > 5:
            loop_duration = random.randrange(5, 15) / 10 * self.glob_speed
            # print("B5 loop duration = ", loop_duration)
            return loop_duration
        else:
            # print('B5 no loop')
            return 0

    def end_time_calc(self, duration):
        # returns the end time for loops
        now_time = time.time()
        return now_time + duration