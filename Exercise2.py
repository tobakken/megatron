#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import random


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

obstacle_sensor = UltrasonicSensor(Port.S4)

touch_sensor = TouchSensor(Port.S2)

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

megatron = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=114)


# Write your program here.
ev3.speaker.beep(frequency = 100)

switch = False
loop = True

while loop:

    if(touch_sensor.pressed()):
        ev3.speaker.say("Exercise two")
        switch = not switch
        wait(1000)

    while switch:

        if obstacle_sensor.distance() < 50:
            megatron.straight(-100)

            megatron.turn(random.randint(-100,100))

        if(touch_sensor.pressed()):
            megatron.stop()
            switch = False
            loop = False
            break

        megatron.drive(100, 0)
        
ev3.speaker.say("Exercise done")