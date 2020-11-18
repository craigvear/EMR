import tkinter as tk
import config
from time import sleep

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
        self.UPDATE_RATE = 0.1  # matches baud rate of Pioneer SIP sends e.g. every 100 ms
        self.create_widget()
        # self.updater()

    def create_widget(self):

        label_x_ds = tk.Label(master=self.frame, text=f"x_ds = {config.x_ds}")
        label_x_ds.grid(row=0, column=1)

        label_y_ds = tk.Label(master=self.frame, text=f"y_ds = {config.y_ds}")
        label_y_ds.grid(row=1, column=1)

        label_z_ds = tk.Label(master=self.frame, text=f"y_ds = {config.z_ds}")
        label_z_ds.grid(row=2, column=1)

        # label_left_wheel = tk.Label(master=self, text=f"Left Wheel Vel = {config.L_VEL}")
        # label_left_wheel.grid(row=3, column=4)
        #
        # label_right_wheel = tk.Label(master=self, text=f"Right Wheel Vel = {config.R_VEL}")
        # label_right_wheel.grid(row=4, column=4)

    def updater(self):
        self.window.update()
        print('ui refresh')
        # sleep(self.UPDATE_RATE)

    def terminate(self):
        global running
        print ('terminator!!!')
        # self.destroy()
        # exit()
        running = False


if __name__ == '__main__':
    gui = GUI()

    while True:
        gui.updater()
        sleep(0.1)