#!/usr/bin/env pybricks-micropython
from BroBot import BroBot
from pybricks.tools import wait

# Initiate EV3 & BroBot
brobot = BroBot()

brobot.calibrate()
wait(1000)
brobot.ev3.speaker.beep(frequency = 999)
brobot.wait_for_button()
brobot.drive_loop()