#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time, random



# Create your objects here.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
left_sensor = ColorSensor(Port.S4) 
right_sensor = ColorSensor(Port.S2)

execute_program = True

debug_mode = False

no_line = False

RED_ON_WHITE = 57
RED_ON_BLACK = 5

GREEN_ON_WHITE = 55
GREEN_ON_BLACK = 4

BLUE_ON_WHITE = 100
BLUE_ON_BLACK = 10

RED = (RED_ON_WHITE + RED_ON_BLACK)/2
GREEN = (GREEN_ON_WHITE + GREEN_ON_BLACK)/2
BLUE = (BLUE_ON_WHITE + BLUE_ON_BLACK)/2

turn_rate = 5
drive_speed = 30

ev3 = EV3Brick()
megatron = DriveBase(left_motor, right_motor, wheel_diameter=55, axle_track=127)


# TODO Increase turn radius while outside black line
# Write your program here.
ev3.speaker.beep()
start_time = time.time()

while (debug_mode):
    execute_program = False
    right_red, right_green, right_blue = right_sensor.rgb()
    left_red, left_green, left_blue = left_sensor.rgb()
    right_is_black = right_red < RED or right_green < GREEN or right_blue < BLUE
    left_is_black = left_red < RED or left_green < GREEN or left_blue < BLUE
    print("right Red: {}, right Green: {}, right Blue: {},".format(right_red, right_green, right_blue))
    print("left Red: {}, left green: {}, left blue: {}".format(left_red, left_green, left_blue))
    print(str(right_is_black + left_is_black))


while True:   
    while (no_line):
        turn_rate = 80
        drive_speed = 50
        right_red, right_green, right_blue = right_sensor.rgb()
        left_red, left_green, left_blue = left_sensor.rgb()
        right_is_black = right_red < RED or right_green < GREEN or right_blue < BLUE
        left_is_black = left_red < RED or left_green < GREEN or left_blue < BLUE
        if not right_is_black and not left_is_black:
            megatron.drive(drive_speed, turn_rate)
        if left_is_black or right_is_black:
            wait(100)
            execute_program = True
            no_line = False


    
    while (execute_program):
        turn_rate = 120
        drive_speed = 200 
        right_red, right_green, right_blue = right_sensor.rgb()
        left_red, left_green, left_blue = left_sensor.rgb()
        right_is_black = right_red < RED or right_green < GREEN or right_blue < BLUE
        left_is_black = left_red < RED or left_green < GREEN or left_blue < BLUE

        if not right_is_black and not left_is_black:
            megatron.drive(drive_speed, 0)
        elif right_is_black and left_is_black:
            megatron.drive(drive_speed, 0)
        elif left_is_black:
            megatron.drive(50, -turn_rate)
            start_time = time.time()
        elif right_is_black:
            megatron.drive(50, turn_rate)
            start_time = time.time()
    

        if time.time() - start_time >= 3:
            start_time = time.time()
            execute_program = False
            no_line = True
        