import UI
import NN
import numpy as np
import pickle

x = UI.runRender()

wbfile = open('weights_and_biases', 'rb')
wb = pickle.load(wbfile)
wbfile.close()

z = NN.NNout([[x] for y in x.values()])

answer = np.where( z == z.max() )

print(answer[0][0])
