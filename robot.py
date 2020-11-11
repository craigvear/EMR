import time
import config
from random import randrange
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play

"""
takes the stored variables in config, and mixes then then smooths output
"""
class Robot(): # smooths the data as a thread class
    def __init__(self):
        # audio source variables
        audio_file = ('data/bill_evans_intro.mp3')
        self.audio = AudioSegment.from_mp3(audio_file)
        self.audio_len = self.audio.duration_seconds * 1000
        print('audio length (ms) = ', self.audio_len)
        print("Roboting, baby")

        # temp moving vars
        self.old_left = 0
        self.old_left_sound = 0
        self.old_right = 0
        self.old_right_sound = 0

    def robot(self, data_density):
        # calc duration into ms from density
        self.data_duration = data_density

        # calculate derivation in data for each wheel
        bot_move_left, bot_move_right = self.calc_deviation()

        # # grabs raw data from config file
        # bot_move_left = config.left_wheel_move_from_smoothing
        # bot_move_right = config.right_wheel_move_from_smoothing

        # robot.set_motors(bot_move_left, bot_move_right)
        print('moving robot', bot_move_left, bot_move_right)
        self.sound(bot_move_left, bot_move_right)

    def calc_deviation(self):
        # sets up temp vars for current params
        left = config.left_wheel_move_from_smoothing
        right = config.right_wheel_move_from_smoothing

        # subtracts new from old and difference = wheel move
        bot_move_left = left - self.old_left
        bot_move_right = right - self.old_right

        # make old vars the current move vars
        config.old_left = bot_move_left
        config.old_right = bot_move_right

        return bot_move_left, bot_move_right

    def sound(self, bot_move_left, bot_move_right):
        # round incoming values
        bot_move_left = round(bot_move_left, 3)
        bot_move_right = round(bot_move_right, 3)

        # calc possible length of sample = audio length (secs) - interval (secs)
        poss_length = int(self.audio_len - self.data_duration)

        # left wheel sounding
        # calc start position
        start_pos_ms = self.calc_start_point(bot_move_left, poss_length)

        # send params to play func
        self.play_sound(start_pos_ms)

        # right wheel sounding
        # calc start position
        start_pos_ms = self.calc_start_point(bot_move_right, poss_length)

        # send params to play func
        self.play_sound(start_pos_ms)


        #
        #
        # # if changes or not to number
        # if bot_move_left_round == self.old_left_sound:
        #     self.old_left_sound = bot_move_left_round
        # else:
        #     # calc start position
        #     start_pos_ms = self.calc_start_point(bot_move_left, poss_length)
        #
        #     # send params to play func
        #     self.play_sound(start_pos_ms)
        #
        #     # makes old value = new
        #     self.old_left_sound = bot_move_left_round
        #
        # if bot_move_right_round == self.old_right_sound:
        #     self.old_right_sound = bot_move_right_round
        # else:
        #     # calc start position
        #     start_pos_ms = self.calc_start_point(bot_move_right, poss_length)
        #
        #     # send params to play func
        #     self.play_sound(start_pos_ms)
        #
        #     # makes old value = new
        #     self.old_right_sound = bot_move_right_round

        # wait because its using simple_audio which only starts play
        # time.sleep(self.interval)

    def play_sound(self, start_pos):
        # adds a bit of overlap with audio threading
        dur_ms = self.data_duration # + 100
        end_pos_ms = start_pos + dur_ms
        print('play params = ', start_pos, dur_ms, end_pos_ms)

        if end_pos_ms > self.audio_len * 1000:
            end_pos_ms = self.audio_len * 1000 - 100

        # concats slicing datain ms
        audio_slice = self.audio[start_pos: end_pos_ms]

        # plays audio
        try:
            play(audio_slice)
        except:
            print(f'################   error start pos {start_pos}, end pos {end_pos_ms}')

        # # pause as its simpleaudio and only starts
        # time.sleep(dur_ms / 1000)

    def calc_start_point(self, incoming, poss_length):
        # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

        # poss_length_ms = poss_length * 1000

        start_pos = (((incoming - -1) * ((poss_length) - 0)) / (1 - -1)) + 0

        # tidy up extremes to avoid SIGKILL errors
        if start_pos > poss_length:
            start_pos = poss_length - 1000
        if start_pos < 0:
            start_pos = 0
        print (f'incoming = {incoming},  poss length = {poss_length} start position from new calc = {start_pos}')
        return start_pos



if __name__ == '__main__':
    bot = Robot()

    while True:
        # calc rate of change random 30 * 15 in ms
        data_density = (randrange(30) + 1) * 15
        print(f'F data density in ms = {data_density}')

        bot.robot(data_density)

        time.sleep(data_density/ 1000)
