from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time

class BroBot():
    def __init__(self):
        left_motor = Motor(Port.B)
        right_motor = Motor(Port.C)
        self.brobot = DriveBase(left_motor, right_motor, wheel_diameter=55, axle_track=127)
        self.left_color_sensor = ColorSensor(Port.S4)
        self.right_color_sensor = ColorSensor(Port.S2)

        self.ev3 = EV3Brick()

        self.RED_ON_WHITE = 57
        self.RED_ON_BLACK = 5

        self.GREEN_ON_WHITE = 55
        self.GREEN_ON_BLACK = 4

        self.BLUE_ON_WHITE = 100
        self.BLUE_ON_BLACK = 10

        self.RED = (self.RED_ON_WHITE + self.RED_ON_BLACK) // 2
        self.GREEN = (self.GREEN_ON_WHITE + self.GREEN_ON_BLACK) // 2
        self.BLUE = (self.BLUE_ON_WHITE + self.BLUE_ON_BLACK) // 2

        self.start_time = time.time()
        self.execute_program = True
        self.no_line = False

    def calibrate(self):
        self.ev3.screen.print("Calibrating...\nL-SENSOR: WHITE\nR-SENSOR: BLACK\nPUSH A BUTTON\nTO CONTINUE")
        while True:
            if self.ev3.buttons.pressed():
                break
            continue
        rgb = self.left_color_sensor.rgb() + self.right_color_sensor.rgb()

        self.RED_ON_WHITE = rgb[0]
        self.GREEN_ON_WHITE = rgb[1]
        self.BLUE_ON_WHITE = rgb[2]

        self.RED_ON_BLACK = rgb[3]
        self.GREEN_ON_BLACK = rgb[4]
        self.BLUE_ON_BLACK = rgb[5]

        self.RED = (self.RED_ON_WHITE + self.RED_ON_BLACK) // 2
        self.GREEN = (self.GREEN_ON_WHITE + self.GREEN_ON_BLACK) // 2
        self.BLUE = (self.BLUE_ON_WHITE + self.BLUE_ON_BLACK) // 2

    def is_black(self, color_sensor):
        (red, green, blue) = color_sensor.rgb()
        if red < self.RED and green < self.GREEN and blue < self.BLUE:
            return True
        else:
            return False

    def look_for_line(self):
        turn_rate = 80
        drive_speed = 50

        right_is_black = self.is_black(self.right_color_sensor)
        left_is_black = self.is_black(self.left_color_sensor)

        if not right_is_black and not left_is_black:
            self.brobot.drive(drive_speed, turn_rate)
        if left_is_black or right_is_black:
            wait(100)
            self.execute_program = True
            self.no_line = False

    def drive_loop(self):
        self.start_time = time.time()

        while True:
            while self.no_line:
                self.look_for_line()

            while self.execute_program:
                self.run()



    def run(self):
        turn_rate = 90
        drive_speed = 250

        right_is_black = self.is_black(self.right_color_sensor)
        left_is_black = self.is_black(self.left_color_sensor)

        if not right_is_black and not left_is_black:
            self.brobot.drive(drive_speed, 0)
        elif right_is_black and left_is_black:
            self.execute_program = False
            self.no_line = True
        elif left_is_black:
            self.brobot.drive(drive_speed/2, -turn_rate)
            self.start_time = time.time()
        elif right_is_black:
            self.brobot.drive(drive_speed/2, turn_rate)
            self.start_time = time.time()

        if time.time() - self.start_time >= 4:
            self.start_time = time.time()
            self.execute_program = False
            self.no_line = True
