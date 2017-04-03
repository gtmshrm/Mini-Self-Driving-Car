"""
Controller module for robot which includes an api
for robot's motion
"""
import os
from time import gmtime, strftime, sleep, time
from util import motor, servo
from pynput import keyboard
import pandas as pd
import sys

SPEED = 70

class Stack(object):
  def __init__(self):
    self.__items = []

  def push(self, item):
    if item not in self.__items:
      self.__items.append(item)

  def pop(self):
    if not self.isEmpty():
      return self.__items.pop()

  def peek(self):
    if not self.isEmpty():
      return self.__items[-1]

  def isEmpty(self):
    return len(self.__items)==0

# State stack keeps track of which is currently pressed
state_stack = Stack()


class Controller(object):
  """Controller api for robot"""
  def __init__(self):
    self.motor = motor.Motor()
    self.servo = servo.Servo(pin=4)
    self.angle = {'forward': 0, 'forward_left': -1, 'forward_right': 1}
    self.data_stack = pd.DataFrame( columns=['angle', 'action', 'timestamp'])
    self.f_a = True
    self.r_a = True
    self.l_a = True

  def on_press(self, key):
    global SPEED
    try:
      # Speed increase methods are handy when battery is about to be dead
      # increase speed by 2 by arrow up
      if key == keyboard.Key.up:
        if SPEED <= 98:
          SPEED += 2
        self.motor.forward(SPEED)

      # increase speed by 2 by arrow down
      elif key == keyboard.Key.down:
        if SPEED >= 0:
          SPEED -= 2
        self.motor.forward(SPEED)

      # increase speed by 10 by arrow up
      elif key == keyboard.Key.right:
        if SPEED <= 98:
          SPEED += 10
        self.motor.forward(SPEED)

      # increase speed by 10 by arrow down
      elif key == keyboard.Key.left:
        if SPEED >= 0:
          SPEED -= 10
        self.motor.forward(SPEED)

      elif key.char == 'w':
        self.motor.forward(SPEED)
        print(state_stack.peek())
        state_stack.push(self.angle['forward'])
        if self.f_a:
          self.data_stack.loc[len(self.data_stack)] = [self.angle['forward'], 'pressed', time()]
          self.f_a = False


      elif key.char == 'a':
        self.servo.left()
        state_stack.push(self.angle['forward_left'])
        if self.l_a:
          self.data_stack.loc[len(self.data_stack)] = [self.angle['forward_left'], 'pressed', time()]
          self.l_a = False


      elif key.char == 'd':
        self.servo.right()
        state_stack.push(self.angle['forward_right'])
        if self.r_a:
          self.data_stack.loc[len(self.data_stack)] = [self.angle['forward_right'], 'pressed', time()]
          self.r_a = False

      elif key.char == 'q':
        self.motor.stop()
        self.servo.center
        self.servo.stop()
        self.save_and_exit()


    except Exception as e:
      print(e)

  def on_release(self, key):
    try:
      if key.char == 'w':
        self.motor.stop()
        self.data_stack.loc[len(self.data_stack)] = [state_stack.pop(), 'released', time()]
        self.f_a = True

      elif key.char == 'a':
        self.servo.center()
        self.data_stack.loc[len(self.data_stack)] = [state_stack.pop(), 'released', time()]
        self.l_a = True

      elif key.char == 'd':
        self.servo.center()
        self.data_stack.loc[len(self.data_stack)] = [state_stack.pop(), 'released', time()]
        self.r_a = True

    except AttributeError:
      print("You've pressed the wrong key!!!")

  def steer(self):
    with keyboard.Listener(
        on_press=self.on_press,
        on_release=self.on_release) as listener:
      listener.join()

  def save_and_exit(self):
    print("saving")
    self.data_stack.to_csv('data/steer-1.csv', index=False)
    print("exiting")
    sys.exit()


def main():
  drive = Controller()
  drive.steer()

if __name__ == '__main__':
  main()
