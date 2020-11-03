import time
import config

from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play
from random import randrange

"""
takes the stored variables in config, and mixes then then smooths output
"""
class Robot(): # smooths the data as a thread class
    def __init__(self):
        # audio source variables
        audio_file = ('data/jarrett_snippet.wav')
        self.audio = AudioSegment.from_wav(audio_file)
        self.audio_len = self.audio.duration_seconds
        print("Roboting, baby")

    def smooth(self, smoothing_dur, bang_timer, end_time):
        # slide between them at bang_timer ms per step
        # self. bang_timer = bang_timer
        while time.time() < end_time:
            # smoothing algo from Max/MSP slide object
            # y(n) = y(n - 1) + ((x(n) - y(n - 1)) / slide)

            current_l = config.left_wheel_move
            target_l = config.left_raw_data
            current_r = config.right_wheel_move
            target_r = config.right_raw_data

            duration = smoothing_dur
            self.interval = duration / 10

            # number of increments
            noi = duration / self.interval

            # split the delta w/ noi
            increment_value_l = (target_l - current_l) / noi
            increment_value_r = (target_r - current_r) / noi

            # smooth my ass
            for _ in range(int(noi)):
                current_l += increment_value_l
                current_r += increment_value_r
                # make the robot move and sound
                self.robot()
            print(current_l, current_r)

            config.left_wheel_move = current_l
            config.right_wheel_move = current_r


            # # wait for baudrate
            # time.sleep(bang_timer)

    def robot(self):
        # robot.set_motors(config.left_wheel_move, config.right_wheel_move)
        print('moving robot', config.left_wheel_move, config.right_wheel_move)
        self.sound()

    def sound(self):
        # calc start position
        poss_length = int(self.audio_len - (self.interval))
        start_pos_ms = randrange(poss_length * 1000)
        dur_ms = self.interval * 1000
        end_pos_ms = start_pos_ms + dur_ms
        audio_slice = self.audio[start_pos_ms: end_pos_ms]

        play(audio_slice)
        time.sleep(self.interval)
