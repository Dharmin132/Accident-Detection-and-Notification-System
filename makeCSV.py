import csv
from mpu6050 import mpu6050

mpu = mpu6050(0x68)

with open('accel_data.csv', 'w', newline='') as accel_file:

    data = csv.writer(accel_file)

    data.writerow(['x', 'y', 'z'])

    for i in range(1, 1001):

        ac_data = mpu.get_accel_data()

        x = float(ac_data['x'])
        y = float(ac_data['y'])
        z = float(ac_data['z'])

        data.writerow([x, y, z])