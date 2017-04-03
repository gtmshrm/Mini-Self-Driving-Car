"""
Module for generating training and validation data
"""
import cv2
import numpy as np
import pandas as pd
import random
from augmentation import augment_brightness

# Pointers keep track of endpoint of previously loaded batch
train_batch_pointer = 0
val_batch_pointer = 0

# Get image paths and steering angles
train_df = pd.read_csv('../../training_data/train.csv')
xs = train_df.id.values
ys = train_df.angle.values

num_images = len(xs)

# Shuffle list of images
c = list(zip(xs, ys))
random.shuffle(c)
xs, ys = zip(*c)

# Train-Validation 80-20 split
train_xs = xs[:int(len(xs) * 0.8)]
train_ys = ys[:int(len(xs) * 0.8)]

val_xs = xs[-int(len(xs) * 0.2):]
val_ys = ys[-int(len(xs) * 0.2):]

num_train_images = len(train_xs)
num_val_images = len(val_xs)


def LoadTrainBatch(batch_size):
  """Load image and steering angle pair of specifized batch size and

  1. Add random brightness augmentation to make model more robust to different lighting conditions
  2. Add random horizontal flipping to double the size of dataset by flipping image and chaning angle's polarity
  """
  global train_batch_pointer
  x_out = []
  y_out = []
  for i in range(0, batch_size):
    # Load image and steering angle pair at position of train batch pointer
    img = cv2.resize(cv2.imread('../../training_data/final_image_data/'+train_xs[(train_batch_pointer + i) % num_train_images]+'.jpg'), (320,240))
    ang = [train_ys[(train_batch_pointer + i) % num_train_images]]

    # Randomly augment brightness
    img = augment_brightness(img)
    # Random horizontal flipping
    if np.random.randint(2):
      img = np.fliplr(img)
      ang[0] = -ang[0]

    x_out.append(img/255.) # normalize image before appending
    y_out.append(ang)
  train_batch_pointer += batch_size
  return x_out, y_out

def LoadValBatch(batch_size):
  """Load image and steering angle pair of specifized batch size and

  1. Add random brightness augmentation to make model more robust to different lighting conditions
  2. Add random horizontal flipping to double the size of dataset by flipping image and chaning angle's polarity
  """
  global val_batch_pointer
  x_out = []
  y_out = []
  for i in range(0, batch_size):
    # Load image and steering angle pair at position of validation batch pointer
    img = cv2.resize(cv2.imread('../../training_data/final_image_data/'+val_xs[(val_batch_pointer + i) % num_val_images]+'.jpg'), (320,240))
    ang = [val_ys[(val_batch_pointer + i) % num_val_images]]

    # Randomly augment brightness
    img = augment_brightness(img)
    # Random horizontal flipping
    if np.random.randint(2):
      img = np.fliplr(img)
      ang[0] = -ang[0]

    x_out.append(img/255.) # normalize image before appending
    y_out.append(ang)
  val_batch_pointer += batch_size
  return x_out, y_out
