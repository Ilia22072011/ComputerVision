#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from time import sleep
import os
import sys

ev3 = EV3Brick()
motor = Motor(Port.B)

FIFO_PATH = "/tmp/motor_commands"


ev3.screen.print("wait")

try:
    while True:
        with open(FIFO_PATH, "r") as fifo:
            command = fifo.readline().strip()
            if command:
                try:
                    angle = int(command)
                    ev3.screen.print(angle)
                    motor.run_target(800, angle)
                except ValueError:
                    ev3.screen.print("non")
                except Exception as e:
                    ev3.screen.print(e)
            else:
                # Если FIFO пуст, ждем немного
                pass # Или можно использовать time.sleep(0.1) для снижения нагрузки на CPU
        sleep(0.03)
        
except KeyboardInterrupt:
    ev3.screen.print("end")
