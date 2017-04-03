"""
Visualize model predictions from pickled numpy array
"""
import matplotlib.pyplot as plt
import numpy as np
import cv2
import pandas as pd
import scipy.misc

# Epoch and Iteration of the model
EPOCH = 1
ITER = 2528

# Load image paths, ground truth and predictions from pickled numpy array
data=np.load('model-{}-{}.npz'.format(EPOCH,ITER))
angs = data['arr_0']
preds = data['arr_1']
testset = pd.read_csv('/home/gtmshrm/projects/sdrcc/training_data/test.csv').id.values

for i,image in enumerate(testset):
  cur_throttle = (angs[i])*100 # scale by 100 for better visualization
  cur_pred = (preds[i])*100

  # Load the image and resize
  cur_img_array = scipy.misc.imread('/home/gtmshrm/projects/sdrcc/training_data/final_image_data/'+image+'.jpg')
  cur_img_array = cv2.resize(cur_img_array, (480, 320), interpolation=cv2.INTER_CUBIC)

  # Add lines and text on the image
  cv2.putText(cur_img_array, "frame: %s" % str(i), (5,35), cv2.FONT_HERSHEY_SIMPLEX,1,255)
  # Draw green line on image for ground truth
  cv2.line(cur_img_array,(240,300),(int(240+cur_throttle),200),(0,255,0),3)
  # Draw red line on image for predictions
  cv2.line(cur_img_array,(240,300),(int(240+cur_pred),200),(255,0,0),3)

  # Visualize ground truth and prediction
  cv2.imshow('frame', cv2.cvtColor(cur_img_array, cv2.COLOR_RGB2BGR))
  if cv2.waitKey(0) & 0xFF == ord('q'):
    break
