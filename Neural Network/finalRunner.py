import UI
import NN
import numpy as np

x = UI.runRender()

z = NN.NNout([[x] for y in x.values()])

answer = np.where( z == z.max() )

print(answer[0][0])
