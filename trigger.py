from time import sleep
import RPi.GPIO as GPIO
from mpu6050 import mpu6050
#import pandas as pd
import math as m

mpu = mpu6050(0x68)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.OUT, initial=GPIO.LOW)

while True:

    accel_data = mpu.get_accel_data()
    gyro_data = mpu.get_gyro_data()

    rollAngle = gyro_data['z']
    acc_x = accel_data['x']
    acc_y = accel_data['y']
    #acc_z = accel_data['z']
    inMotion = True
    #isTwoWheeler = False

    if acc_x == 0 and acc_y == 0:
        inMotion = False

    elif abs(acc_x) > 1.5:

        for i in range(0, 10):
            GPIO.output(37, GPIO.HIGH)
            sleep(0.1)
            GPIO.output(37, GPIO.LOW)
            sleep(0.1)

        print("Accident Detected!")

        if acc_x < 0:
            print("Front Side Impacted...")
        else:
            print("Back Side Impacted...")

    elif abs(acc_y) > 1.5:

        for i in range(0, 10):
            GPIO.output(37, GPIO.HIGH)
            sleep(0.1)
            GPIO.output(37, GPIO.LOW)
            sleep(0.1)

        print("Accident Detected!")

        if acc_y < 0:
            print("Right Side Impacted...")
        else:
            print("Left Side Impacted...")

    elif rollAngle >= 45:
        if inMotion == True:
            print("Accident Detected!")
