"""
Take sync.csv in each data folder and concat into final.csv
Add mean columns
"""
import collections
import numpy as np
import pandas as pd
import os

DIR = '/home/gtmshrm/projects/training_data/'
data_folders = os.listdir(DIR)
RANGE = (3,15)

# First file
final = pd.read_csv(str(DIR)+'0/sync.csv')

# Append the rest of csv files
for num, folder in enumerate(data_folders):
  try:
    if 'sync.csv' in os.listdir(str(DIR)+folder):
      temp = pd.read_csv(str(DIR)+folder+'/sync.csv', header=None)
      final = pd.concat([final,temp], ignore_index=True)
  except Exception:
    pass

# Add regressive labels (mean of last 3 to 15 steering angles)
# Taking mean of last 'n' steering angles smoothens the angle
# and gives an real valued angle in range 0 to 1
n_mean_labels = []

for i in range(RANGE[0],RANGE[1]):
  x = collections.deque(i*[0], i)
  mean_labels = []
  for angle in final.angle.values:
    x.appendleft(angle)
    mean_labels.append(np.mean(x))
  n_mean_labels.append(mean_labels)

# Add regressive labels to final.csv and save
for i in range(RANGE[0],RANGE[1]):
  final['mean_last_%d_frames'%i] = pd.Series(n_mean_labels[i-RANGE[0]], index=final.index)

final.to_csv(DIR+'final.csv', index=False)
