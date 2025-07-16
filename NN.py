from keras.datasets import mnist
from matplotlib import pyplot
import numpy as np
import random

print("a")
(train_X, train_y), (test_X, test_y) = mnist.load_data()

for i in range(9):  
    pyplot.subplot(330 + 1 + i)
    pyplot.imshow(train_X[i], cmap=pyplot.get_cmap('gray'))
    print(type(train_X[i]))
pyplot.show()

def ReLu(x):
    if x>=0:
        return x
    return 0

class Layer:
    def __innit__(self, size, connections, prev_layer):
        self.size = size
        self.biasVector = vertify([0]*size)
        self.postmatrix = np.array([[random.random() for a in range(prev_layer.size)] for b in range(size)])
        self.previousLayer = prev_layer
        self.nextLayer = None
    def setActNext(self, actfunc=ReLu):
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

def vertify(L):
    return np.array([[x] for x in L])
