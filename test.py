from pydub import AudioSegment

song = AudioSegment.from_mp3("never_gonna_give_you_up.mp3")



# old_x = 100
# target_x = 1000
# ramp_rate = 0.5
#
# print(target_x - old_x)
# print((target_x - old_x) / (ramp_rate * 1000))
# # print(((target_x - old_x) / ramp_rate) * 10)
#
# increment_x = round((target_x - old_x) / (ramp_rate * 1000), 2)
# print (increment_x)
#
#
# # from threading import Thread
# # from queue import Queue
# # from time import sleep, time
# # import config
# # from random import randrange
# #
# # """
# # config defintioins
# # config.temp_x = holding var direct from dataline - needs to be smoothed
# # config.output
# #
# # """
# # class Data_Smoother(Thread): # smooths the data as a thread class
# #     def __init__(self):
# #         Thread.__init__(self)
# #         print("Smoothing, baby")
# #         self.running = True
# #         self.old_x = 0
# #
# #     def run(self):
# #         while self.running:
# #             self.ramp_rate = config.baudrate / 1000  # what is current baudrate - which might change with instances of class
# #             self.calc_x() # calculate starting parameters
# #             # self.old_x = config.raw_x # logs the raw_x(n-1) ready for next smoothing
# #             # todo all others .calc
# #
# #             # define time steps
# #             timer = time() # now time
# #             end_time = timer + self.ramp_rate # end time
# #
# #             while time() < end_time: # for duration of loop
# #                 self.smooth_x() # activate a single step of smoothing, pass increment value from calc
# #                 # todo all other vars
# #                 sleep(0.01)
# #             self.old_x = self.target_x
# #
# #     def calc_x(self): # calculate parameters per loop
# #         self.target_x = config.raw_x  # current target value of raw_x(n)
# #         self.increment_x = round((((self.target_x - self.old_x) / self.ramp_rate) * 10), 2)  # what is the step
# #         print ('params are == ', self.old_x, self.target_x, self.increment_x)
# #
# #     def smooth_x(self): # calculate 1 step of smoothing and updates config param
# #         config.temp_x = self.old_x + self.increment_x
# #         print(config.temp_x)
# #
# #
# # class DataAtoms(Thread): # bangs out the working atoms from the smoothing thread above
# #     def __init__(self):
# #         Thread.__init__(self)
# #         print("banging out atoms, man")
# #         self.running = True
# #
# #     """these deal with banging out the usable data atoms for movement"""
# #     def run(self):
# #         while self.running:
# #             bang_rate = randrange(150, 1300) / 1000
# #             config.atom_x = round(config.temp_x, 2)
# #             print ('atoms = ', config.atom_x)
# #             print('bang rate ', bang_rate)
# #             # todo all others y, z, freq, amp
# #             sleep(bang_rate)
# #
# #
# # if __name__ == "__main__":
# #     smooth_bot = Data_Smoother()
# #     data_atoms_bot = DataAtoms()
# #     smooth_bot.start()
# #     data_atoms_bot.start()
# #
# #
# #
# #
# # #
# # #
# # #     ramp_rate = 500 # 1/2 second as test in ms
# # #     print ('params = ', old_x, target_x, ramp_rate)
# # #
# # #     range = target_x - old_x
# # #     print('range = ', range)
# # #
# # #     increment = (range / ramp_rate) * 10
# # #     print ('increment = ', increment)
# # #
# # #     output = old_x
# # #
# # #     timer = time.time()
# # #     end_time = timer + (ramp_rate / 1000)
# # #     while time.time() < end_time:
# # #         print (threading.current_thread().name,worker,'output = ', '%.2f' %output)
# # #         output += increment
# # #         time.sleep (0.01)
# # #         # timer += increment
# # #
# # #     old_x = target_x
# # #
# # # # The threader thread pulls an worker from the queue and processes it
# # # def threader():
# # #     while True:
# # #         # gets an worker from the queue
# # #         worker = q.get()
# # #
# # #         # Run the example job with the avail worker in queue (thread)
# # #         exampleJob(worker)
# # #
# # #         # completed with the job
# # #         q.task_done()
# # #
# # #
# # # # Create the queue and threader
# # # q = Queue()
# # #
# # # # how many threads are we going to allow for
# # # for x in range(10):
# # #      t = threading.Thread(target=threader)
# # #
# # #      # classifying as a daemon, so they will die when the main dies
# # #      t.daemon = True
# # #
# # #      # begins, must come after daemon definition
# # #      t.start()
# # #
# # # start = time.time()
# # #
# # # # 20 jobs assigned.
# # # for worker in range(20):
# # #     q.put(worker)
# # #
# # # # wait until the thread terminates.
# # # q.join()
# # #
# # # # with 10 workers and 20 tasks, with each task being .5 seconds, then the completed job
# # # # is ~1 second using threading. Normally 20 tasks with .5 seconds each would take 10 seconds.
# # # print('Entire job took:',time.time() - start)
# # #
# # #
# # #
# # #
# # #
# # #
# # # #
# # # #
# # # #
# # # # from random import randrange
# # # # from numpy import linspace
# # # # from time import sleep, time
# # # # running = True
# # # #
# # # #
# # # # old_x = 200
# # # # #target_x = -20
# # # #
# # # # # ramp_rate = randrange (150, 1300) / 1000
# # # # while running:
# # # #     input_x = input('target number')
# # # #
# # # #     target_x = int(input_x)
# # # #
# # # #     ramp_rate = 400 # 1/2 second as test in ms
# # # #     print ('params = ', old_x, target_x, ramp_rate)
# # # #
# # # #     range = target_x - old_x
# # # #     print('range = ', range)
# # # #
# # # #     increment = (range / ramp_rate) * 10
# # # #     print ('increment = ', increment)
# # # #
# # # #     output = old_x
# # # #
# # # #     timer = time()
# # # #     end_time = timer + (ramp_rate / 1000)
# # # #     while time() < end_time:
# # # #         print ('output = ', '%.2f' %output)
# # # #         output += increment
# # # #         sleep (0.01)
# # # #         # timer += increment
# # # #
# # #     old_x = target_x