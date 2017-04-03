import RPi.GPIO as io
import time


class Motor(object):
  def __init__(self, in1_pin=22, in2_pin=27, delayed=0, mode="pwm", duty_cycle=70, frequency=500, active=1):
    self.in1_pin = in1_pin
    self.in2_pin = in2_pin
    self.delayed = delayed
    self.mode = mode
    self.frequency = frequency
    self.duty_cycle = duty_cycle
    self.active = active
    io.setmode(io.BCM)
    io.setup(self.in1_pin, io.OUT)
    io.setup(self.in2_pin, io.OUT)
    self.pwm = io.PWM(self.in1_pin, self.frequency)

  def forward(self, speed):
    self.pwm.start(speed)
    io.output(self.in2_pin, False)

  def stop(self):
    self.pwm.stop()
    io.output(self.in1_pin, False)
    io.output(self.in2_pin, False)
