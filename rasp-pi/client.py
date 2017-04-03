"""
Client side module which sends images (one at a time)
to the server and receives predicted steering angle and
turns the steering according to the received angle
"""
import time
import sys
import struct
import socket
import picamera
import numpy as np
import io
from collect_data import util

# ********* Sending *************

client_socket = socket.socket()
print('bef con')
client_socket.connect(('192.168.0.7', 8000))
print('aft con')

# *********************************

connection = client_socket.makefile('wb')

# ********* Recieving *************

server_socket = socket.socket()
server_socket.bind(('192.168.0.4', 8001))
server_socket.listen(0)

# *********************************

# Start motor and servo PWM
m = util.motor.Motor()
s = util.servo.Servo(4)

recieve_connection = server_socket.accept()[0]

try:
  with picamera.PiCamera() as camera:
		# Calibrate pi cam
    camera.resolution = (320,240)
    camera.framerate = 10

    stream = io.BytesIO()
    
		# Send images continuously using video_port
		# video_port speeds up the transmission speed more than 5x
    for image in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
			# Send image byte stream to server
      connection.write(struct.pack('<l',stream.tell()))
      connection.flush()
      print(stream, type(stream))
      stream.seek(0)
      connection.write(stream.read())
      
      stream.seek(0)
      stream.truncate()


      # Receive steering angle from server
      steering_angle = float(recieve_connection.recv(1024).decode("ascii"))
      print("Received steering angle --> ", steering_angle)

			# Turn front servo by steering_angle
      s.turn(steering_angle)
			# Move forward with speed 60
      m.forward(60)
  

except KeyboardInterrupt:
	# Stop motor and servo PWM
  m.stop()
  s.center()
  s.stop()
	# Close all socket connections 
  connection.close()
  client_socket.close()
  sys.exit(-1)

finally:
  print('closing sockets')
	# Stop motor and servo PWM
  m.stop()
  s.center()
  s.stop()
	# Close all socket connections 
  connection.close()
  client_socket.close()
