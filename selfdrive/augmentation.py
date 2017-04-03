"""
Module for adding augmentations to the training data

TODO: add random shifts and rotations for path correction
"""
import numpy as np
import cv2


def augment_brightness(image):
  """Randomly augment brightness in image"""
  image1 = cv2.cvtColor(image,cv2.COLOR_RGB2HSV)
  random_bright = .25+np.random.uniform()
  image1[:,:,2] = image1[:,:,2]*random_bright
  image1 = cv2.cvtColor(image1,cv2.COLOR_HSV2RGB)
  return image1

