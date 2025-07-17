from keras.datasets import mnist
from matplotlib import pyplot
import pickle

print("a")
(train_X, train_y), (test_X, test_y) = mnist.load_data()

print(train_X[1])