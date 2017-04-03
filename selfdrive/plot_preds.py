"""
Plot model preditions v/s ground truth graph

Note: For getting a better sense of point predictions,
      plot not more than 200 data points in a single graph
"""
import matplotlib.pyplot as plt
import numpy as np

# Model epoch and iteration as an identity for model checkpoint
EPOCH = 1
ITER = 2528

# Load serialized numpy array containing model predictions on test set
data=np.load('model-{}-{}.npz'.format(EPOCH,ITER))
angs = data['arr_0']
preds = data['arr_1']

# Starting and Ending data point from test set
# (difference between start and end should ideally be <=200)
start = 22100
end = 22300

# Plot graph
ground_truth, = plt.plot(angs[start:end], label="Ground truth")
pred, = plt.plot(preds[start:end], label="Predicted angle")
plt.legend(handles=[ground_truth,pred])

plt.show()
