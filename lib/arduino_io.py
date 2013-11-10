#!/usr/bin/python

import json
import serial
import time

class arduino():

    def __init__(self, timeout=5, writeTimeout=5):
        self.serial = serial.Serial(port='/dev/tty.arduino', baudrate=9600)
        time.sleep(3)

    def read_drink_info_from_serial(self):
        try:
            self.serial.write("syn_drink_info")
            input = self.serial.readline()
            drink_info = json.loads(input)
            return drink_info
        except SerialTimeoutException as e:
            return None
