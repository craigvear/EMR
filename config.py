""" config all global variable to share across classes"""

# global interrupt flag
affect_interrupt = False

# variable for dataset parsing
x_ds = 0.5
y_ds = 0.5
z_ds = 0.5
freq_ds = 0.5
amp_ds = 0.5

temp_x_ds = 0.5
temp_y_ds = 0.5
temp_z_ds = 0.5
temp_freq_ds = 0.5
temp_amp_ds = 0.5

# variable for ML parsing
x_ml = 0.5
y_ml = 0.5
z_ml = 0.5

# variable for ML live parsing
x_ml_live = 0.5
y_ml_live = 0.5
z_ml_live = 0.5

temp_x_ml = 10
temp_y_ml = 10
temp_z_ml = 10

# variables for motor movement
right_raw_data_from_affect_mix = 0.5
left_raw_data_from_affect_mix = 0.5
left_wheel_move_from_smoothing = 0.5
right_wheel_move_from_smoothing = 0.5

# affect vars
affect_interrupt = False
mix_interrupt = False
