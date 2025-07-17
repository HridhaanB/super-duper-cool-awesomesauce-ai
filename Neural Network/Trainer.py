from keras.datasets import mnist
from matplotlib import pyplot
import pickle
import NN
print("a")
(train_X, train_y), (test_X, test_y) = mnist.load_data()

print(train_X[1])

#set in layer
inlayer = []

wb = NN.getWeightsAndBiases(inlayer)

wbfile = open('weights_and_biases', 'ab')

# source, destination
pickle.dump(wb, wbfile)
wbfile.close()