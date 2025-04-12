#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from time import sleep
import os
import sys

ev3 = EV3Brick()
motor = Motor(Port.A)
mB = Motor(Port.B)
mC = Motor(Port.C)

FIFO_PATH = "/tmp/motor_commands"


try:
    while True:
        with open(FIFO_PATH, "r") as fifo:
            command = fifo.readline().strip()
            if command:
                try:
                    mB.run(100)
                    mC.run(100)
                    angle = int(command)
                    motor.run_target(800, angle)
                except ValueError:
                    pass
                except Exception as e:
                    pass
            else:
                # Если FIFO пуст, ждем немного
                pass # Или можно использовать time.sleep(0.1) для снижения нагрузки на CPU
        sleep(0.03)
        
except KeyboardInterrupt:
    pass