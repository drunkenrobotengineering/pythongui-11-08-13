pythongui-11-08-13
==================

This is a test repo while I'm working on development for the kegerator ui.  Eventually this'll be copied over to a prod repo.



Necessary libraries:
pySerial (can be installed with "pip install pyserial")

must have arduino connected at /dev/tty.arduino with baud rate 9600

Help for the arduino side of the program can be found at https://github.com/adafruit/Adafruit-Flow-Meter/blob/master/Adafruit_FlowMeter.pde

Arduino communication protocol:
-RPi sends a syn
-Arduino responds with the following string:
{"1":{"c":"#"},"2":{"c":"#"}}
Where # is a number of ml consumed from the given tap
This response must be sent within a second or two.
-RPi sends an ack
-Arduino subtracts the amount transmitted from its internal counter