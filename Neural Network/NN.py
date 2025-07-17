from keras.datasets import mnist
from matplotlib import pyplot
import numpy as np
import random

#print("a")
(train_X, train_y), (test_X, test_y) = mnist.load_data()

for i in range(9):  
    pyplot.subplot(330 + 1 + i)
    pyplot.imshow(train_X[i], cmap=pyplot.get_cmap('gray'))
    print(train_y[i])
pyplot.show()
print(len(train_X))
def ReLu(x):
    if x>=0:
        return x
    return 0

class Layer:
    def __innit__(self, size, pLayer):
        self.size = size
        self.biasVector = vertify([0]*size)
        self.postmatrix = np.array([[random.random() for a in range(pLayer.size)] for b in range(size)])
        self.previousLayer = pLayer
        self.nextLayer = None
        self.zVector = None
    def setActNext(self, actfunc=ReLu):
        self.setZNext()
        self.nextLayer.setAct(actfunc(self.nextLayer.zVector))
    def setAct(self, activation):
        self.actVector = activation
    def setNext(self, next):
        self.nextLayer = next
        next.previousLayer = self
    def setZNext(self):
        self.nextLayer.zVector = self.postmatrix.dot(self.actVector) + self.nextLayer.biasVector

def NNout(inLay, Grid):
    inLay.setAct(vertify([Grid[x] for x in Grid]))
    while inLay.nextLayer!=None:
        inLay.setActNext()
        inLay = inLay.nextLayer
    return inLay.actVector()

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
    dadz = np.where(lastLayer.zVector<=0, 0, 1)
    dzdw = lastLayer.previousLayer.actVector
    dzdb = 1
    dCdw = dCda*dadz*dzdw
    dCdb = dCda*dadz*dzdb
    part = np.vstack((dCdw, dCdb))
    while lastLayer.previousLayer.previousLayer is not None:
        lastLayer = lastLayer.previousLayer
        dCda = dCda*dadz
        dadz = np.where(lastLayer.zVector<=0, 0, 1)
        dzdw = lastLayer.previousLayer.actVector
        dCdw = dCda*dadz*dzdw
        dCdb = dCda*dadz*dzdb
        part = np.vstack((dCdw, dCdb, part))
    return part

def get_averaged_gradient(lastLayer, inLay, window):
    L = len(train_y)
    endgrad = vertify([0 for _ in range(10000)]) #change to get real len
    cutoff = 500
    for x, y in zip(train_X[window*cutoff:(window+1)*cutoff], train_y[window*cutoff:(window+1)*cutoff]):
        endgrad += get_gradient(lastLayer, inLay)
    return endgrad

input_layer = Layer(784, None)
hidden_layer1 = Layer(200, input_layer)
hidden_layer2 = Layer(80, hidden_layer1)
output_layer = Layer(10, hidden_layer2)
input_layer.setNext(hidden_layer1)
hidden_layer1.setNext(hidden_layer2)
hidden_layer2.setNext(output_layer)
