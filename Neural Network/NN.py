from keras.datasets import mnist
from matplotlib import pyplot
import numpy as np
import random
import pickle

print("a")
(train_X, train_y), (test_X, test_y) = mnist.load_data()

wbfile = open('weights_and_biases', 'rb')
wb = pickle.load(wbfile)
for keys in wb:
    print(keys, '=>', wb[keys])
wbfile.close()

for i in range(9):  
    pyplot.subplot(330 + 1 + i)
    pyplot.imshow(train_X[i], cmap=pyplot.get_cmap('gray'))
    print(type(train_X[i]))
pyplot.show()

def ReLU(x):
    if x>=0:
        return x
    return 0

class Layer:
    def __innit__(self, size, connections, prev_layer):
        self.size = size
        if wb is None:
            self.postmatrix = np.array([[random.random() for a in range(prev_layer.size)] for b in range(size)])
            self.biasVector = vertify([0]*size)
        else:
            self.postmatrix = wb[0]
            self.biasVector = wb[1]
        self.previousLayer = prev_layer
        self.nextLayer = None
    def setActNext(self, actfunc=ReLU):
        self.nextLayer.setAct(actfunc(self.postmatrix.dot(self.actVector) + self.nextLayer.biasVector))
    def setAct(self, activation):
        self.actVector = activation
    def setNext(self, next):
        self.nextLayer = next
        next.previousLayer = self

def NNout(inLay, Grid):
    inLay.setAct(vertify([Grid[x] for x in Grid]))
    while inLay.nextLayer!=None:
        inLay.setActNext()
        inLay = inLay.nextLayer
    return inLay.actVector()

def update(gradient, inLayer):
    gradient_index = 0
    layer = inLayer
    while layer.nextLayer is not None:
        for j in range(len(layer.postmatrix)):
            for k in range(len(layer.postmatrix[i])):
                layer.postmatrix[j][k] += gradient[gradient_index]
                gradient_index += 1
        for j in range(len(layer.biasVector)):
            layer.biasVector[j] += gradient[gradient_index]
            gradient_index += 1
        layer = layer.nextLayer

def getWeightsAndBiases(inLayer):
    layer = inLayer
    weights = []
    biases = []
    while layer.nextLayer is not None:
        weights.append(layer.postmatrix)
        biases.append(layer.biasVector)
        layer = layer.nextLayer
    return weights, biases

def vertify(L):
    return np.array([[x] for x in L])
