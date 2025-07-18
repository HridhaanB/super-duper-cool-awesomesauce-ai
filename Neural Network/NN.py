from keras.datasets import mnist
from matplotlib import pyplot
import numpy as np
import random
import math

#print("a")
(train_X, train_y), (test_X, test_y) = mnist.load_data()

#print(len(train_X))
def sigmoid(x):
    return 1/(1+math.exp(min(x*-1*0.01, 20)))

def ReLU(x):
    return max(0, x)

def sigmoid_derivative(x):
    return sigmoid(x*0.01) * (1 - sigmoid(x*0.01))


class Layer:
    def __init__(self, size, pLayer):
        self.size = size
        self.biasVector = vertify([0.0]*size)
        self.previousLayer = pLayer
        self.nextLayer = None
        self.zVector = None
    def setActNext(self, actfunc=sigmoid):
        self.setZNext()
        self.nextLayer.setAct(np.vectorize(actfunc)(self.nextLayer.zVector))
    def setAct(self, activation):
        self.actVector = activation
    def setNext(self, next):
        self.nextLayer = next
        next.previousLayer = self
        self.postmatrix = np.array([[random.random()*2-1 for a in range(self.size)] for b in range(next.size)])
    def setZNext(self):
        #print(np.dot(self.postmatrix, self.actVector))
        self.nextLayer.zVector = np.dot(self.postmatrix, self.actVector) + self.nextLayer.biasVector

def NNout(inLay, Grid):
    inLay.setAct(vertify([y for x in Grid for y in x]))
    while inLay.nextLayer!=None:
        inLay.setActNext()
        inLay = inLay.nextLayer
        #print(inLay.actVector)
    return inLay.actVector

def vertify(L):
    return np.array([[x] for x in L])

def cost(out_vector, answer):
    return sum((out_vector - answer_vec(answer))**2)/10

def total_cost(inLay):
    tc = []
    for x, y in zip(train_X, train_y):
        tc.append(cost(NNout(inLay)))
    return sum(tc)/len(tc)

def answer_vec(answer):
    return np.array([[1] if x==answer else [0] for x in range(10) ])

def get_gradient(lastLayer, answer):
    dCda = 2*(lastLayer.actVector - answer_vec(answer))
    dadz = np.vectorize(sigmoid_derivative)(lastLayer.zVector)
    dzdw = lastLayer.previousLayer.actVector
    dzdb = 1
    dCdw = vertify(np.outer(dCda*dadz, dzdw).flatten())
    dCdb = dCda*dadz*dzdb
    part = np.vstack((dCdw, dCdb))
    while lastLayer.previousLayer.previousLayer is not None:
        lastLayer = lastLayer.previousLayer
        #print((dCda*dadz).flatten())
        dCda = vertify((lastLayer.postmatrix * np.repeat(dCda*dadz, lastLayer.size, axis=1)).sum(axis=0))
        dadz = np.vectorize(sigmoid_derivative)(lastLayer.zVector)
        dzdw = lastLayer.previousLayer.actVector
        dCdw = vertify(np.outer(dCda*dadz, dzdw).flatten())
        dCdb = dCda*dadz*dzdb
        #print(dCda)
        #print(dCdb)
        part = np.vstack((dCdw, dCdb, part))
    return part*1000

def get_averaged_gradient(lastLayer, inLay, window):
    L = len(train_y)
    endgrad = vertify([0.0 for _ in range(173890)]) #change to get real len
    cutoff = 10
    for x, y in zip(train_X[window*cutoff:(window+1)*cutoff], train_y[window*cutoff:(window+1)*cutoff]):
        NNout(inLay, x/255)
        endgrad += get_gradient(lastLayer, y)
    print(endgrad/len(endgrad))
    return endgrad/len(endgrad)

def update(gradient, inLayer):
    gradient_index = 0
    layer = inLayer
    while layer.nextLayer is not None:
        for j in range(len(layer.postmatrix)):
            for k in range(len(layer.postmatrix[0])):
                layer.postmatrix[j][k] -= gradient[gradient_index]
                gradient_index += 1
        if layer.previousLayer is not None:
            for j in range(len(layer.biasVector)):
                layer.biasVector[j] -= gradient[gradient_index]
                gradient_index += 1
        layer = layer.nextLayer

def getStuff(inLayer):
    if inLayer.nextLayer is not None:
        return [inLayer.biasVector, inLayer.postmatrix] + getStuff(inLayer.nextLayer)
    return [inLayer.biasVector]

input_layer = Layer(784, None)
hidden_layer1 = Layer(200, input_layer)
hidden_layer2 = Layer(80, hidden_layer1)
output_layer = Layer(10, hidden_layer2)
input_layer.setNext(hidden_layer1)
hidden_layer1.setNext(hidden_layer2)
hidden_layer2.setNext(output_layer)
