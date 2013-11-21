#!/usr/bin/python

import json
import serial
from serial import *
import time

class arduino():
    serial_port = "/dev/tty.arduino"
#    serial_port = "/dev/tty.usbmodem1411"
    def __init__(self, timeout=5, writeTimeout=5):
        self.serial = serial.Serial(port=self.serial_port, baudrate=19200)
        time.sleep(3)

    def read_drink_info_from_serial(self):
        try:
            self.serial.write("1")
            input = self.serial.readline()
            print("Received serial input: " + input)
            drink_info = json.loads(input)
            return drink_info
        except SerialTimeoutException as e:
            return None

class fake_arduino():
    # For testing when I don't have an Arduino handy
    one = 0.0
    two = 50.0
    def __init__(self):
        pass

    def read_drink_info_from_serial(self):
        self.one = self.one + 20
        self.two = self.two * 1.02
        drink_info={"1":{},"2":{}}
        drink_info["1"]["c"] = self.one
        drink_info["2"]["c"] = self.two
        return drink_info
