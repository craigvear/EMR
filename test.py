# config.left_wheel_move = current value
# config.left_raw_data = target
# result [y(n)] = y(n - 1) + ((x(n) - y(n - 1)) / slide)
# current value will then = result
# config.left_wheel_move = current value


current = 1.2
target = 4
target2 = 1
duration = 3
interval = 0.1

# number of increments
noi = duration / interval
# print(noi)

# split the delta w/ noi
increment_value = (target - current) / noi
# print(increment_value)

print(current)

for _ in range(int(noi)):
    # current
    current += increment_value
print(current)

# split the delta w/ noi
increment_value = (target2 - current) / noi
# print(increment_value)

for _ in range(int(noi)):
    # current
    current += increment_value
print(current)




# import config
# import random
#
# ml_out_4_mixer = random.randrange(6)
# if ml_out_4_mixer == 0:
#     left_raw = config.x_ml
#
#
# print(ml_out_4_mixer)
#


# import csv
# import random
# import time
#
#
# dataset = 'training/raw_phase1_dataset.csv'
#
# dataset_read_dur = random.randrange(3000, 13000)
# start_time = time.time()
# end_time = start_time + (dataset_read_dur/1000)
#
# # convert current dataset into tuples
# with open(dataset) as f:
#     reader = csv.reader(f)
#     your_list = list(reader)
#
# # print(len(your_list))
#
# my_num = (your_list[3][3])
#
# print(float(my_num))
#
# # print(dataset_read_dur/1000)
# # time.sleep(dataset_read_dur / 1000)