"""
* Take all the image and steering angle data
* Get 1-1 image-angle mapping for each folder
* Save the mapping as foo.csv in each data folder
"""
import os
from matplotlib import pylab
import imageio
import csv
import pickle
import numpy as np
import pandas as pd
import collections


class Stack(object):
  def __init__(self):
    self.__items = []

  def push(self, __item):
    if __item not in self.__items:
      self.__items.append(__item)

  def pop(self):
    if not self.isEmpty():
      return self.__items.pop()

  def peek(self):
    return self.__items[-1]

  def isEmpty(self):
    return len(self.__items) == 0

  def print_stack(self):
    print(self.__items)

def bucket(timestamp, angle_df):
  try:
    return angle_df['angle'][(timestamp>=angle_df['start_timestamp'])&(timestamp<=angle_df['end_timestamp'])].values[0]
  except:
    return np.nan

RANGE = (3,15)
DIR = '/home/gtmshrm/projects/gsoc-self-driving-rc-car/training_data/'
train_folders = os.listdir(DIR)

for folder in train_folders:
  if os.path.isdir(DIR+folder) and ('video1.mp4' in os.listdir(DIR+folder)) and (not 'sync.csv' in os.listdir(DIR+folder)):
    # File-contents: steer-1.csv --> steering angle (direction), action and timestamp
    print(folder)
    data_stack = pd.read_csv(DIR+folder+'/steer-1.csv')

    # File-contents: start-ts-1.pkl --> start time of video recording
    with open(DIR+folder+'/start-ts-1.pkl', 'rb') as f:
      start_time = pickle.load(f)

    # Load mp4 video
    filename = DIR+folder+'/video1.mp4'
    vid = imageio.get_reader(filename,  'ffmpeg')

    # Extract start and end time for each action
    angle_df = pd.DataFrame(columns=['angle', 'start_timestamp', 'end_timestamp'])
    stack = Stack()
    for i in range(len(data_stack)):
      angle,action,timestamp = data_stack.loc[i]['angle'],data_stack.loc[i]['action'],data_stack.loc[i]['timestamp']
      if action == 'pressed':
        stack.push([angle, timestamp])
      elif action == 'released':
        start_ts = stack.pop()[1]
        end_ts = timestamp
        angle_df.loc[len(angle_df)] = [angle, start_ts, end_ts]

    sync_df = pd.DataFrame(columns=['id', 'angle'], dtype = int)
    for num, image in enumerate(vid.iter_data()):
      timestamp = float(num) / 15.
      timestamp += start_time
      if timestamp >= angle_df.loc[0]['start_timestamp'] and timestamp <= angle_df.loc[len(angle_df)-1]['end_timestamp']:
        sync_df.loc[len(sync_df)] = [num, bucket(timestamp, angle_df)]

    # Remove records where angle is NaN
    sync_df = sync_df.dropna().reset_index(drop=True)

    for i in range(len(sync_df)):
      pylab.imsave(DIR+'final_image_data/#'+folder+'-'+str(int(sync_df.id.values[i]))+'.jpg', vid.get_data(int(sync_df.id.values[i])))
      sync_df.loc[i,'id'] = '#'+folder+'-'+str(int(sync_df.id.values[i]))
      print(i, sync_df.values[i])
      pylab.close()
    print(folder)

    sync_df = sync_df.dropna().reset_index(drop=True)
    n_mean_labels = []

    for i in range(RANGE[0],RANGE[1]):
      x = collections.deque(i*[0], i)
      mean_labels = []
      for angle in sync_df.angle.values:
        x.appendleft(angle)
        mean_labels.append(np.mean(x))
      n_mean_labels.append(mean_labels)

    # Add regressive labels to final.csv and save
    for i in range(RANGE[0],RANGE[1]):
      sync_df['mean_last_%d_frames'%i] = pd.Series(n_mean_labels[i-RANGE[0]], index=sync_df.index)

    sync_df.to_csv(DIR+folder+"/sync.csv", index=False)

