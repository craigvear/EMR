"""LSTM training script for use with the Creative AI dataset.
Dataset must be pre-compiled into a single .csv"""

"""thank you https://stackabuse.com/solving-sequence-problems-with-lstm-in-keras-part-2/
https://towardsdatascience.com/weather-forecasting-a-deep-learning-approach-7ecddff0fa71
https://medium.com/analytics-vidhya/weather-forecasting-with-recurrent-neural-networks-1eaa057d70c3
"""

# 1. load all modules and libraries
from keras.models import Sequential
from keras.layers import Bidirectional
from keras.layers import Dense
from keras.layers import LSTM, Dropout
import numpy as np
from pandas import read_csv

# 2. establish the data sets and numeric environment
# fix random seed for reproducibility
np.random.seed(7)

# load the dataset
df = read_csv('good_dataset_mini.csv', header=None)
col_name = ['id', 'limb', 'x', 'y', 'z', 'freq', 'amp']
df.columns = col_name
# apply filter function
# A) just the features we want
# df = df.filter(['x', 'y', 'z', 'freq', 'amp'])
# B) all rows with amp values greater than 0.1 (i.e. has a sound) & freq below 2500
# df = df[df['amp'] > 0.1] # ignoring this for now as I want non-events to be learnt
df = df[df['freq'] < 2500]
#  OPTIONAL C) only "body" data
df = df[df['limb'] == '/Hand_Right']
df = df.filter(['x', 'y', 'z', 'freq', 'amp']) # just the operational data

dataset = df.values # just the values
# dataset = dataset.astype('float32') # unified as float
print (dataset)

# 3. split into train and test sets
train_size = int(len(dataset) * 0.67) # 67% Train
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
# print('train    ', train)
# print('test    ', test)

# convert an array of values into a dataset matrix
def create_dataset(dataset, n_future=1, n_past=1):
    x_train = []
    y_train = []

    for i in range (n_past, len(dataset)-n_past-1):
        for num in range(n_past):
            x_train.append(dataset[i-num]) # incoming array
            y_train.append(dataset[i]) # linked to output prediction
        # print(x_train, y_train)
    x_train, y_train = np.array(x_train), np.array(y_train)
    print(x_train.shape[0])
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    return np.array(x_train), np.array(y_train)


    # dataX, dataY = [], []
    # for i in range(len(dataset)-look_back-1):
    #     a = dataset[i:(i+look_back), 0]
    #     print('a   ', a)
    #     dataX.append(a)
    #     print('X   ', dataX)
    #     dataY.append(dataset[i + look_back, 0])
    #     print('Y   ', dataY)
    # return numpy.array(dataX), numpy.array(dataY)

# 4. reshape into X=t and Y=t+5
n_future = 1  # next 4 events todo sort out lookback
n_past = 10  # Past 30 events
trainX, trainY = create_dataset(train, n_future, n_past)
testX, testY = create_dataset(test, n_future, n_past)

# reshape input to be [samples, time steps, features]
# trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1)) # 83480 features, 5 time steps, 5 features
# print (trainX.shape[0], trainX.shape[1], trainX.shape[2])
# testX = np.reshape(testX, (testX.shape[0], testX.shape[1], 1))

# 5. create and fit the LSTM network
model = Sequential()
model.add(Bidirectional(LSTM(64, return_sequences=True), input_shape=(trainX.shape[1], 1))) # input shape is 5 timesteps, 1-3d feature
model.add(Dropout(0.2))
model.add(LSTM(64, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(64, return_sequences=True))  # returns a sequence of vectors of dimension
model.add(Dropout(0.2))
model.add(LSTM(64))
model.add(Dropout(0.2))
model.add(Dense(units=5)) # how many outputs as predictions

model.compile(loss='mean_squared_error', optimizer='adam', metrics='accuracy')
model.fit(trainX, trainY, epochs=1000, batch_size=32, verbose=1)

model.save('LSTM_Bidirectional_64x4_1000epochs-5in-5out_model.h5')
print ('saved')

