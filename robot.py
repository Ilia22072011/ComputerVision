#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from time import sleep
import os
import sys

ev3 = EV3Brick()
motor = Motor(Port.A)
mb = Motor(Port.B)
mc = Motor(Port.C)

FIFO_PATH = "/tmp/motor_commands"
last = 0
try:
    while True:
        with open(FIFO_PATH, "r") as fifo:
            command = fifo.readline().strip()
            if command:
                angle = int(command)
                if angle == 222:
                    mb.run(150)
                    mc.run(150)
                else:
                    motor.run_target(1000, angle)
                    print(angle)
                    last = angle
            else:
                # Если FIFO пуст, ждем немного
                pass # Или можно использовать time.sleep(0.1) для снижения нагрузки на CPU
        sleep(0.03)
        
except KeyboardInterrupt:
    pass