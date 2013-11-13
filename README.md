pythongui-11-08-13
==================

This is a test repo while I'm working on development for the kegerator ui.  Eventually this'll be copied over to a prod repo.

-Look into PIL and ImageTK for displaying beer labels

Necessary libraries:
pySerial (can be installed with "pip install pyserial")
eventually, probably boto (can be installed with "easy_install boto")

must have arduino connected at /dev/tty.arduino with baud rate 19200

Base for the arduino side of the program can be found at https://github.com/adafruit/Adafruit-Flow-Meter/blob/master/Adafruit_FlowMeter.pde

Current Arduino communication protocol:
-RPi send a byte over serial
-Arduino responds with the following string:
{"1":{"c":"#"},"2":{"c":"#"}}
Where # is the total amount consumed from that tap.
Eventually this response will include a snippet specifying when the flowmeters started up.  If the arduino has gone down since the last time it reported to the RPi, its last total should become a baseline volume that's added to all future values from the Arduino.