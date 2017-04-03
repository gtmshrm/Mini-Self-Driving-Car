import time
import pigpio


class Servo(object):
  def __init__(self, pin):
    self.pin = pin
    self.pi = pigpio.pi() # Connect to local Pi.
    self.extreme_turn_pwm = 200
    self.center_pwm = 2150
    self.left_pwm = self.center_pwm - self.extreme_turn_pwm
    self.right_pwm = self.center_pwm + self.extreme_turn_pwm

  def center(self):
    self.pi.set_servo_pulsewidth(self.pin, self.center_pwm);
    time.sleep(.02)

  def left(self):
    self.pi.set_servo_pulsewidth(self.pin, self.left_pwm);
    time.sleep(.02)

  def right(self):
    self.pi.set_servo_pulsewidth(self.pin, self.right_pwm);
    time.sleep(.02)

  def turn(self, angle):
    self.pi.set_servo_pulsewidth(self.pin, self.center_pwm+angle*self.extreme_turn_pwm);
    time.sleep(.02)

  def stop(self):
    self.pi.set_servo_pulsewidth(self.pin, 0);
