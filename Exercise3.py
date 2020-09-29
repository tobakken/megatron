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

line_sensor = ColorSensor(Port.S3)

touch_sensor = TouchSensor(Port.S2)

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

megatron = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=114)

#Program

ev3.speaker.beep(frequency = 1000)

#Sjekk sensor
while True:
    print(line_sensor.reflection())
    wait(200)


#Threshold
BLACK = 80
WHITE = 2
threshold = BLACK+WHITE/2

#Fart
DRIVE_SPEED = 100

#Sving-radius
PROPORTIONAL_GAIN = 1.2

while True:
    #Hvor langt fra streken er vi?
    deviation = line_sensor.reflection() - threshold

    #Hvis vi er på streken vil turn_rate bli 0
    turn_rate = deviation * PROPORTIONAL_GAIN

    megatron.drive(DRIVE_SPEED, turn_rate)

    wait(20)



