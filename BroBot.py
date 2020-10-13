from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time

class BroBot():
    def __init__(self):
        
        self.brobot = DriveBase(left_motor=Motor(Port.B), right_motor=Motor(Port.C), wheel_diameter=55, axle_track=127)
        self.left_color_sensor, self.right_color_sensor = ColorSensor(Port.S4), ColorSensor(Port.S2)
        self.ev3 = EV3Brick()
        self.RED, self.GREEN, self.BLUE = 50, 50, 50 

        self.start_time = time.time()
        self.execute_program = True
        self.no_line = False  

    def calibrate(self):
        self.ev3.screen.print("COLOR CALIBRATION:\nL-SENSOR: WHITE\nR-SENSOR: BLACK\nPUSH A BUTTON\nTO CONTINUE")
        self.wait_for_button()
        self.ev3.screen.clear()

        RED_ON_WHITE, GREEN_ON_WHITE, BLUE_ON_WHITE = self.left_color_sensor.rgb()
        RED_ON_BLACK, GREEN_ON_BLACK, BLUE_ON_BLACK = self.right_color_sensor.rgb()

        self.RED = (RED_ON_WHITE + RED_ON_BLACK) // 2
        self.GREEN = (GREEN_ON_WHITE + GREEN_ON_BLACK) // 2
        self.BLUE = (BLUE_ON_WHITE + BLUE_ON_BLACK) // 2

    def wait_for_button(self):
        while True:
            if self.ev3.buttons.pressed():
                break
            continue

    def is_black(self, color_sensor):
        (red, green, blue) = color_sensor.rgb()
        if red < self.RED and green < self.GREEN and blue < self.BLUE:
            return True
        else:
            return False

    def look_for_line(self):
        turn_rate = 50
        drive_speed = 100

        right_is_black = self.is_black(self.right_color_sensor)
        left_is_black = self.is_black(self.left_color_sensor)

        if not right_is_black and not left_is_black:
            self.brobot.drive(drive_speed, turn_rate)
        if left_is_black or right_is_black:
            wait(drive_speed/1.75)
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
        drive_speed = 175

        right_is_black = self.is_black(self.right_color_sensor)
        left_is_black = self.is_black(self.left_color_sensor)

        if not right_is_black and not left_is_black:
            self.brobot.drive(drive_speed, -5)
        elif right_is_black and left_is_black:
            wait(drive_speed/1.75)
            self.execute_program = False
            self.no_line = True
        elif left_is_black:
            self.brobot.drive(drive_speed/2, -turn_rate)
            self.start_time = time.time()
        elif right_is_black:
            self.brobot.drive(drive_speed/2, turn_rate)
            self.start_time = time.time()

        if time.time() - self.start_time >= 10:
            self.start_time = time.time()
            self.execute_program = False
            self.no_line = True
