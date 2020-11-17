import tkinter as tk
import config

class GUI():
    """ GUI """

    def __init__(self):
        """ Initialize the Frame"""
        print('building GUI')

        self.window = tk.Tk()
        self.frame = tk.Frame()
        self.window.title("Robot Control")
        self.window.geometry("700x500")
        self.frame.grid()
        self.frame.rowconfigure([0, 1, 2, 3, 4], minsize=100, weight=1)
        self.frame.columnconfigure([0, 1, 2, 3, 4], minsize=75, weight=1)
        self.UPDATE_RATE = 100  # matches baud rate of Pioneer SIP sends e.g. every 100 ms
        self.slow_loop = self.UPDATE_RATE / 10  # slows down pulse to 1/10th UPDATE_RATE e.g. sending every second
        self.create_widget()
        # self.updater()

    def create_widget(self):

        label_x_ds = tk.Label(master=self.frame, text=f"x_ds = {config.x_ds}")
        label_x_ds.grid(row=0, column=4)

        label_y_ds = tk.Label(master=self.frame, text=f"y_ds = {config.y_ds}")
        label_y_ds.grid(row=2, column=4)

        label_z_ds = tk.Label(master=self.frame, text=f"y_ds = {config.z_ds}")
        label_z_ds.grid(row=2, column=4)

        # label_left_wheel = tk.Label(master=self, text=f"Left Wheel Vel = {config.L_VEL}")
        # label_left_wheel.grid(row=3, column=4)
        #
        # label_right_wheel = tk.Label(master=self, text=f"Right Wheel Vel = {config.R_VEL}")
        # label_right_wheel.grid(row=4, column=4)

    def updater(self):
        self.after(self.UPDATE_RATE, self.updater)

    def terminate(self):
        global running
        print ('terminator!!!')
        # self.destroy()
        # exit()
        running = False