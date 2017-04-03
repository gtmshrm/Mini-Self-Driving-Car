"""
Module for evaluating Mean Squared Error (MSE)
"""
import numpy as np

def mse(targets,preds):
  """Calculate mean squared error for target and prediction vector"""
  return np.sum(np.power(targets-preds,2))/len(targets)

# Model epoch and iteration as an identity of model checkpoint
EPOCH = 1
ITER = 2528

# Load angle and prediction vectors with specified model checkpoint
data=np.load('model-{}-{}.npz'.format(EPOCH,ITER))

angs = data['arr_0']
preds = data['arr_1']

print(mse(angs,preds))


