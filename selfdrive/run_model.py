"""
Evaluate model's prediction on test set and serialize it
into multidimensional numpy array
"""
import collections
import cv2
import matplotlib.pyplot as plt
import model
import numpy as np
import os
import pandas as pd
import tensorflow as tf
import tqdm

# Model epoch and iteration as identity for model checkpoint
EPOCH = 1
ITER = 2528

# Start interactivate session and restore trained model
sess = tf.InteractiveSession()
saver = tf.train.Saver()
saver.restore(sess, "save/model-{}-{}.ckpt".format(EPOCH,ITER))

# Load image paths and ground truth for steering angles
test_df = pd.read_csv('../../../training_data/test.csv')
imgs = test_df.id.values
angs = test_df.angle.values

preds = []

for i in tqdm.tqdm(range(len(test_df))):
  img_path = "../../../training_data/final_image_data/"+imgs[i]+".jpg"
  image = cv2.resize(cv2.imread(img_path), (320,240)) / 255.
  # Predict steering angle
  angle = model.y.eval(feed_dict={model.x: [image], model.keep_prob: 1.0})[0][0]
  preds.append(angle)


preds=np.array(preds)
np.savez('model-flip-{}-{}.npz'.format(EPOCH,ITER),angs,preds)
