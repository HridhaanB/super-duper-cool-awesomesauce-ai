import UI
from NN import *
import numpy as np
import pickle

x = UI.runRender()

wbfile = open('weights_and_biases', 'rb')
wb = pickle.load(wbfile)
wbfile.close()

input_layer.biasVector = wb[0]
input_layer.postmatrix = wb[1]
hidden_layer1.biasVector = wb[2]
hidden_layer1.postmatrix = wb[3]
hidden_layer2.biasVector = wb[4]
hidden_layer2.postmatrix = wb[5]
output_layer.biasVector = wb[6]

z = NNout(input_layer, [[y] for y in x.values()])


answer = np.where( z == z.max() )


print(answer[0][0])
