"""
This class listens to the live feed and responds with affect linking.
This changes the mix and sends flags for change
"""

from random import randrange
import config
import time

class Affect():
    # debug toggles
    debug_mix = False
    debug_listen = False

    def __init__(self, glob_speed):
        print('affect object init')
        self.glob_speed = glob_speed

        # initiates object variables
        self.right_raw_data_from_affect_mix = 0
        self.left_raw_data_from_affect_mix = 0

        # self.CHUNK = 2 ** 11
        # self.RATE = 11025
        # self.p = pyaudio.PyAudio()
        # self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, input=True,
        #                           frames_per_buffer=self.CHUNK)

    def smooth(self):
        """smooths the output from the mixer"""
        # grabs current wheel settings from config
        current_l = config.left_wheel_move_from_smoothing
        current_r = config.right_wheel_move_from_smoothing

        # grabs output from mixer
        target_r = config.right_raw_data_from_affect_mix
        target_l = config.left_raw_data_from_affect_mix

        # number of intervals
        # noi = slide / 10

        # smoothing algo from Max/MSP slide object
        # y(n) = y(n - 1) + ((x(n) - y(n - 1)) / slide)

        # split the delta
        increment_value_l = (target_l - current_l) / 20
        increment_value_r = (target_r - current_r) / 20
        # print (f' inc = {increment_value_l}')

        # output result back out to config
        config.left_wheel_move_from_smoothing = current_l + increment_value_l
        config.right_wheel_move_from_smoothing = current_r + increment_value_r

    def mixing(self):
        # randomly mixes the data streams to the smoothing/wheels
        left_out = randrange(6) # todo reduced to exclude ml-live
        if left_out == 0:
            config.left_raw_data_from_affect_mix = config.x_ds
        elif left_out == 1:
            config.left_raw_data_from_affect_mix = config.y_ds
        elif left_out == 2:
            config.left_raw_data_from_affect_mix = config.z_ds
        elif left_out == 3:
            config.left_raw_data_from_affect_mix = config.x_ml
        elif left_out == 4:
            config.left_raw_data_from_affect_mix = config.y_ml
        elif left_out == 5:
            config.left_raw_data_from_affect_mix = config.z_ds
        elif left_out == 6:
            config.left_raw_data_from_affect_mix = config.x_ml_live
        elif left_out == 7:
            config.left_raw_data_from_affect_mix = config.y_ml_live
        else:
            config.left_raw_data_from_affect_mix = config.z_ml_live
        if self.debug_mix:
            print('Left matrix out is ', left_out)

        right_out = randrange(6) # todo reduced to exclude ml-live
        if right_out == 0:
            config.right_raw_data_from_affect_mix = config.x_ds
        elif right_out == 1:
            config.right_raw_data_from_affect_mix = config.y_ds
        elif right_out == 2:
            config.right_raw_data_from_affect_mix = config.z_ds
        elif right_out == 3:
            config.right_raw_data_from_affect_mix = config.x_ml
        elif right_out == 4:
            config.right_raw_data_from_affect_mix = config.y_ml
        elif left_out == 5:
            config.right_raw_data_from_affect_mix = config.z_ds
        elif left_out == 6:
            config.right_raw_data_from_affect_mix = config.x_ml_live
        elif left_out == 7:
            config.right_raw_data_from_affect_mix = config.y_ml_live
        else:
            config.right_raw_data_from_affect_mix = config.z_ml_live
        if self.debug_mix:
            print('Right matrix out is ', right_out)


    def mix_control(self):
        # how long to stay in a mix 1 - 4 seconds
        rnd_timing = (randrange(1000, 4000) / 1000) * self.glob_speed
        if self.debug_listen:
            print('E - affect mixing', rnd_timing, (int(rnd_timing * 100)))

        # hold mix until affect bang or end of cycle
        for _ in range(int(rnd_timing) * 100):
            # break if loud sound affects flow
            if config.affect_interrupt:
                time.sleep(0.1)
                break
            # break if medium sound affects flow
            elif config.mix_interrupt:
                time.sleep(0.1)
                break
            time.sleep(0.01)

    # def listening(self):
    #     data = np.frombuffer(self.stream.read(self.CHUNK), dtype=np.int16)
    #     # transform the output level to 0 - 100
    #     peak = (np.average(np.abs(data)) * 2) / 100
    #     if self.debug_listen:
    #         print('peak level = ', peak)
    #     return peak

    # def snd_listen_terminate(self):
    #     self.stream.stop_stream()
    #     self.stream.close()
    #     self.p.terminate()

    def bang_mix_out(self):
        config.x_ds = config.temp_x_ds
        config.y_ds = config.temp_y_ds
        config.z_ds = config.temp_z_ds
        config.freq_ds = config.temp_freq_ds
        config.amp_ds = config.temp_amp_ds

        config.x_ml = config.temp_x_ml
        config.y_ml = config.temp_y_ml
        config.z_ml = config.temp_z_ml
        if self.debug_mix:
            print('BANGED MIX OUTPUTS')

if __name__ == '__main__':

    bot = Affect(1)

    while True:
        peak = bot.listening()
        print(peak)




        # config.left_raw_data_from_affect_mix = randrange(-100, 100)/ 100
        # config.right_raw_data_from_affect_mix = randrange(-100, 100)/ 100
        #
        # print('random  are ', config.left_raw_data_from_affect_mix, config.right_raw_data_from_affect_mix)
        # bot.smooth()
        #
        # print('configs are ', config.left_wheel_move_from_smoothing, config.right_wheel_move_from_smoothing)
        # time.sleep(1)
