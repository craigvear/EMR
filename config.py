""" config all global variable"""

dataset = 'training/raw_phase1_dataset.csv'
working_datafile_name = 'empty'
baudrate = 0.1

# variable for dataset parsing
x_ds = 0
y_ds = 0
z_ds = 0

# variable for ML parsing
x_ml = 0
y_ml = 0
z_ml = 0

# variables for motor movement
right_raw_data = 0
left_raw_data = 0
left_wheel_move = 0
right_wheel_move = 0

old_left = 0
old_right = 0

#working variables for robot motors
atom_id = 0
atom_limb = 'empty'
atom_x = 10
atom_y = 10
atom_z = 10
atom_freq = 10
atom_amp = 10

# temp vairiables for smoothing and banging
temp_x = 100
temp_y = 100
temp_z = 100
temp_freq = 100
temp_amp = 100

# raw variables output by the data coll queries
raw_id = 100
raw_limb = 'empty'
raw_x = 10
raw_y = 0
raw_z = 0
raw_freq = 0
raw_amp = 0
