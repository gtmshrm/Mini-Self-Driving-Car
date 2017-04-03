"""
Server side module which receives images from the robot(client) of the
road in front of it. It feeds the image to the model and the model
outputs a steering angle which is sent to the robot(client)
"""
import io
import socket
import struct
import numpy as np
import collections
import cv2
from PIL import Image
import time
import os
import tensorflow as tf
from gautam import model

# Model checkpoint to be loaded
MODEL = 'save/model-1024.ckpt'

# Restore model from its checkpoint
sess = tf.InteractiveSession()
saver = tf.train.Saver()
saver.restore(sess, MODEL)

# ********* Recieving *************

server_socket = socket.socket()
server_socket.bind(('192.168.0.7', 8000))
server_socket.listen(0)

# *********************************

connection = server_socket.accept()[0].makefile('rb')

# Wait for server socket on the client to start
time.sleep(2)

# ********* Sending *************

client_socket = socket.socket()
client_socket.connect(('192.168.0.4', 8001))
print('client connection with server')

# *********************************

send_connection = client_socket.makefile('wb')


try:
  while True:
    prev_time = time.time()
    image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]

    # Get image as byte stream
    image_stream = io.BytesIO()
    image_stream.write(connection.read(image_len))

    # Load the received image, reshape and resize it as per the input shape of model
    image_stream.seek(0)
    image = np.asarray(Image.open(image_stream).convert('L')).reshape(1,480,640,1)
    image = cv2.resize(image, (320,240)) / 255.

    # Predict steering angle
    pred = model.y.eval(feed_dict={model.x: [image], model.keep_prob: 1.0})[0][0]

    # Send steering angle to robot
    client_socket.send("{0:.2f}".format(pred).encode())
    print("Sent Pred -->", pred)

    # Estimated prediction (time including receiving delay of image)
    print("Prediction took -->", time.time()-prev_time)


finally:
  # Close all socket connections
  connection.close()
  server_socket.close()
