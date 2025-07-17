from keras.datasets import mnist
from matplotlib import pyplot
import pickle
from NN import *

for win in range(100):
    update(get_averaged_gradient(output_layer, input_layer, win), input_layer)
print(getStuff(input_layer))
