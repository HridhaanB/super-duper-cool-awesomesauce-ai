from keras.datasets import mnist
from matplotlib import pyplot

print("a")
(train_X, train_y), (test_X, test_y) = mnist.load_data()

for i in range(9):  
    pyplot.subplot(330 + 1 + i)
    pyplot.imshow(train_X[i], cmap=pyplot.get_cmap('gray'))
    print(type(train_X[i]))
pyplot.show()

def ReLu(x):
    pass