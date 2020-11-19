import time
import config
from random import randrange
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play

"""
takes the stored variables in config, and mixes then then smooths output
"""
class Robot(): # smooths the data as a thread class
    debug_robot = False

    def __init__(self, wheel, glob_density):
        self.wheel = wheel
        self.glob_density = glob_density
        if self.wheel == 'left':
            self.instrument = 'bass'
        else:
            self.instrument = 'piano'

        # audio source variables
        if self.wheel == 'left':
            audio_file = ('data/misha_lacy_off_minor.wav')

        else:
            audio_file = ('data/hdi_bass_1.wav')
        self.audio = AudioSegment.from_wav(audio_file)
        self.audio_len = self.audio.duration_seconds * 1000
        print('audio length  (ms) = ', self.audio_len)

        print("Roboting, baby", self.wheel, self.instrument)

        # # temp moving vars
        # self.old_left = 0
        # self.old_left_sound = 0
        # self.old_right = 0
        # self.old_right_sound = 0

    def robot(self, data_density):
        # calc duration into ms from density
        self.data_duration = data_density

        # calculate derivation in data for each wheel
        # bot_move_left, bot_move_right = self.calc_deviation()

        # # grabs raw data from config file
        if self.wheel == 'left':
            bot_move_wheel = config.left_raw_data_from_affect_mix
        else:
            bot_move_wheel = config.right_raw_data_from_affect_mix

        # robot.set_motors(bot_move_left, bot_move_right)
        if self.debug_robot:
            print('moving robot', self.wheel, bot_move_wheel)
        self.sound(bot_move_wheel)

    # def calc_deviation(self):
    #     # sets up temp vars for current params
    #     left = config.left_wheel_move_from_smoothing
    #     right = config.right_wheel_move_from_smoothing
    #
    #     # subtracts new from old and difference = wheel move
    #     bot_move_left = left - self.old_left
    #     bot_move_right = right - self.old_right
    #
    #     # make old vars the current move vars
    #     config.old_left = bot_move_left
    #     config.old_right = bot_move_right
    #
    #     return bot_move_left, bot_move_right

    def sound(self, bot_move_wheel):
        # round incoming values
        # bot_move_left = round(bot_move_left, 3)
        # bot_move_right = round(bot_move_right, 3)

        # calc possible length of sample = audio length (secs) - interval (secs)
        # if self.wheel == 'left':
        poss_length = int(self.audio_len - self.data_duration)
        # else:
        #     poss_length = int(self.audio_len_piano - self.data_duration)

        # left wheel sounding
        # calc start position
        start_pos_ms = self.calc_start_point(bot_move_wheel, poss_length)

        # send params to play func

        self.play_sound(start_pos_ms)



        # # right wheel sounding
        # # calc start position
        # start_pos_ms_right = self.calc_start_point(bot_move_right, poss_length_piano)
        #
        # # send params to play func
        # self.play_sound('piano', start_pos_ms_right)

    def play_sound(self, start_pos):
        # adds a bit of overlap with audio threading
        dur_ms = self.data_duration # + 100
        end_pos_ms = start_pos + (dur_ms / randrange(1, 10))
        if self.debug_robot:
            print('play params = ', start_pos, dur_ms, end_pos_ms)

        if end_pos_ms > self.audio_len * 1000:
            end_pos_ms = self.audio_len * 1000 - 100

        # concats slicing data in ms
        # if se /lf.instrument == 'bass':
        audio_slice = self.audio[start_pos: end_pos_ms]
        # else:
        #     audio_slice = self.audio_piano[start_pos: end_pos_ms]

        # plays audio
        try:
            play(audio_slice)
        except:
            print(f'################   error start pos {start_pos}, end pos {end_pos_ms}')


    def calc_start_point(self, incoming, poss_length):
        # new_value = ( (old_value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min
        start_pos = ( (incoming - -2) / (2 - -2) ) * (poss_length - 0) + 0
        # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
        # start_pos = (((incoming - -2) * (poss_length - 0)) / (2 - -2)) + 0

        # tidy up extremes to avoid SIGKILL errors
        if start_pos > poss_length:
            start_pos = poss_length - 1000
        if start_pos < 0:
            start_pos = 0
        if self.debug_robot:
            print (f'incoming = {incoming},  poss length = {poss_length} start position from new calc = {start_pos}')
        return start_pos



if __name__ == '__main__':
    bot = Robot('left', 1)

    while True:
        # calc rate of change random 30 * 15 in ms
        data_density = (randrange(30) + 1) * 15
        print(f'F data density in ms = {data_density}')

        bot.robot(data_density)

        time.sleep(data_density/ 1000)
