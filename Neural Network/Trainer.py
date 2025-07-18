from keras.datasets import mnist
from matplotlib import pyplot
import pickle
from NN import *

for win in range(30):
    update(get_averaged_gradient(output_layer, input_layer, win), input_layer)
    print(win)
#print(getStuff(input_layer))

print(NNout(input_layer, test_X[0]))
print(test_y[0])


wb = getStuff(input_layer)

wbfile = open('weights_and_biases', 'ab')

# source, destination
pickle.dump(wb, wbfile)
wbfile.close()