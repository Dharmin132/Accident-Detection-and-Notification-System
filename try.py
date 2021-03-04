from mpu6050 import mpu6050
import time

mpu = mpu6050(0x68)

while True:
    print("Temp: "+str(mpu.get_temp()))
    print()