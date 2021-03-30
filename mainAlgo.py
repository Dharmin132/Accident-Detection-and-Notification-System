from time import sleep
import RPi.GPIO as GPIO
from mpu6050 import mpu6050
#import pandas as pd
import csv
import math as m

mpu = mpu6050(0x68)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.OUT, initial=GPIO.LOW)


def makeCSV(x, y, len, path):

    with open(path, 'w') as accel_file:

        data = csv.writer(accel_file)
        data.writerow(['x', 'y'])

        for i in range(0, len):
            data.writerow([x, y])


def notify():

    print(" ")
    print(" ") 

    for i in range(0, 100):
        GPIO.output(37, GPIO.HIGH)
        sleep(0.1)
        GPIO.output(37, GPIO.LOW)
        sleep(0.1)

    print("Accident Detected!")
    print(" ")


def collisionSeverity(G, fs, len1, len2, d, a):

    # temp1 = [0.0]*len1
    # temp2 = [0.0]*len1
    # temp3 = [0.0]*len1
    x18 = [0.0]*len1
    xcfc18 = [0.0]*len2
    vel = [0.0]*len2

    end1 = 0
    end2 = 0

    # temp1[0] = A[0]*G[0]
    # temp1[1] = A[0]*G[1] + A[1]*G[0] - B[1]*temp1[0]

    # for i in range(2, len1):
    #     temp1[i] = A[0]*G[i] + A[1]*G[i-1] + A[2]*G[i-2] - B[1]*temp1[i-1] - B[2]*temp1[i-2]

    # i = len1 - 1

    # for j in range(0, len1):
    #     temp2[j] = temp1[i]
    #     i -= 1

    # temp3[0] = A[0]*temp2[0]
    # temp3[1] = A[0]*temp2[1] + A[1]*temp2[0] - B[1]*temp3[0]

    # for i in range(2, len1):
    #     temp3[i] = A[0]*temp2[i] + A[1]*temp2[i-1] + A[2]*temp2[i-2] - B[1]*temp3[i-1] - B[2]*temp3[i - 2]

    i = len1 - 1

    for j in range(0, len1):
        #x18[j] = temp3[i]
        x18[j] = G[i]
        i -= 1

    xcfc18[0] = x18[0]

    for i in range(1, len2):
        xcfc18[i] = x18[d*i]

    vel[0] = (xcfc18[0] * 0.0098) / fs

    for i in range(1, len2):
        vel[i] = ((xcfc18[i]*0.0098) / fs) + vel[i-1]

    for i in range(0, len2):
        vel[i] = vel[i]*3.6

    j = 0

    for i in range(1, len2):
        if (abs(xcfc18[i]) > abs(xcfc18[j])):
            j = i

    if(a == 'x'):
        px = xcfc18[j]
        chk2 = abs(0.05*px)

    else:
        py = xcfc18[j]
        chk2 = abs(0.05*py)

    for i in range(j, -1, -1):
        if (abs(xcfc18[i]) <= 1.5):
            end1 = i
            break

    for i in range(j, len2):
        if (abs(xcfc18[i]) <= chk2):
            end2 = i
            break

    if(a == 'x'):
        dvx = vel[end2] - vel[end1]
    else:
        dvy = vel[end2] - vel[end1]

    if(a == 'x'):
        return px, dvx
    else:
        return py, dvy

def severityHelper(fs, len1, x, y):

    dvx = 0.0
    dvy = 0.0
    px = 0.0
    py = 0.0
    p = 0.0
    dv = 0.0

    # A = [0.0]*3
    # B = [0.0]*3

    # wa = 0.1178/fs
    # wa += (wa**3)/3

    # A[0] = (wa**2)/(1 + 1.4142*wa + wa**2)
    # A[1] = 2*A[0]
    # A[2] = A[0]

    # B[0] = 1
    # B[1] = (2*(wa**2) - 2)/(1 + 1.4142*wa + wa**2)
    # B[2] = (1 - 1.4142*wa + wa**2)/(1 + 1.4142*wa + wa**2)

    d = int(m.floor(fs))
    len2 = int(m.floor((len1 + d - 1) / d))

    sevx = 1
    sevy = 1
    sevz = 1

    # px, dvx = collisionSeverity(x, fs, A, B, len1, len2, d, 'x')
    # py, dvy = collisionSeverity(y, fs, A, B, len1, len2, d, 'y')

    px, dvx = collisionSeverity(x, fs, len1, len2, d, 'x')
    py, dvy = collisionSeverity(y, fs, len1, len2, d, 'y')

    p = m.sqrt(px**2 + py**2)
    dv = m.sqrt(dvx**2 + dvy**2)

    L2 = int((abs(px) >= 5 and abs(px) <= 13) or (abs(dvx) >= 12.8 and abs(dvx) <= 22.5))
    L3 = int((abs(px) > 13) or (abs(dvx) > 22.5))

    if (L3 == 1):
        sevx = 3
    elif (L3 == 0 and L2 == 1):
        sevx = 2
    elif (abs(px) < 3):
        sevx = 0

    L2 = int((abs(py) >= 5 and abs(py) <= 13) or (abs(dvy) >= 12.8 and abs(dvy) <= 22.5))
    L3 = int((abs(py) > 13) or (abs(dvy) > 22.5))

    if (L3 == 1):
        sevy = 3
    elif (L3 == 0 and L2 == 1):
        sevy = 2
    elif (abs(py) < 3):
        sevy = 0

    L2 = (p >= 5 and p <= 13) or (dv >= 12.8 and dv <= 22.5)
    L3 = (p > 13) or (dv > 22.5)

    if (L3 == 1):
        sevz = 3
    elif (L3 == 0 and L2 == 1):
        sevz = 2

    # notify()
    # print("TYPE: Collision")

    if sevz == 3:
        notify()
        print("TYPE: Collision")
        print("OVERALL SEVERITY: Extreme")
        print(" ")
        print("*DIRECTIONAL ANALYSIS*")
    elif sevz == 2:
        notify()
        print("TYPE: Collision")
        print("OVERALL SEVERITY: High")
        print(" ")
        print("*DIRECTIONAL ANALYSIS*")
    else:
        #print("OVERALL SEVERITY: Moderate")
        pass

    # if sevz == 1:
    #     print("SENDER: User \n")
    # else:
    #     #print("SENDER: Auto \n")
    #     pass

    if px < 0:
        if sevx == 3:
            makeCSV(x, y, len1, 'front.csv')
            print("FRONT: Extreme")
        elif sevx == 2:
            makeCSV(x, y, len1, 'front.csv')
            print("FRONT: High")
        elif sevx == 1:
            makeCSV(x, y, len1, 'front.csv')
            print("FRONT: Moderate")
        else:
            #print("FRONT: --")
            pass

        #print("REAR: --")

    else:
        if sevx == 3:
            makeCSV(x, y, len1, 'rear.csv')
            print("REAR: Extreme")
        elif sevx == 2:
            makeCSV(x, y, len1, 'rear.csv')
            print("REAR: High")
        elif sevx == 1:
            makeCSV(x, y, len1, 'rear.csv')
            print("REAR: Moderate")
        else:
            #print("REAR: --")
            pass

        #print("FRONT: --")

    if py < 0:
        if sevy == 3:
            makeCSV(x, y, len1, 'right.csv')
            print("SIDE(RIGHT): Extreme")
        elif sevy == 2:
            makeCSV(x, y, len1, 'right.csv')
            print("SIDE(RIGHT): High")
        elif sevy == 1:
            makeCSV(x, y, len1, 'right.csv')
            print("SIDE(RIGHT): Moderate")
        else:
            #print("SIDE(RIGHT): --")
            pass

        #print("SIDE(LEFT): --")

    else:
        if sevy == 3:
            makeCSV(x, y, len1, 'left.csv')
            print("SIDE(LEFT): Extreme")
        elif sevy == 2:
            makeCSV(x, y, len1, 'left.csv')
            print("SIDE(LEFT): High")
        elif sevy == 1:
            makeCSV(x, y, len1, 'left.csv')
            print("SIDE(LEFT): Moderate")
        else:
            #print("SIDE(LEFT): --")
            pass

        #print("SIDE(RIGHT): --")

    print(" ")
    print(" ")
    print(" ")


def main():

    fs = 20
    len1 = 2000
    temp = 0
    c = 0
    x2 = 0.0
    y2 = 0.0

    acc_x = [0.0]*len1
    acc_y = [0.0]*len1
    acc_z = [0.0]*len1

    while True:

        for i in range(0, len1):

            accel_data = mpu.get_accel_data()
            acc_x[i] = accel_data['x'] + 1.49884
            acc_y[i] = accel_data['y'] + 0.12869
            acc_z[i] = accel_data['z'] + 0.195528

        for i in range(0, len1):

            x2 = acc_x[i]*acc_x[i]
            y2 = acc_y[i]*acc_y[i]

            if (acc_z[i] < 0.5 and abs(acc_y[i] > 0.866)):
                temp += 1

                if (temp == (fs*1000*2)):
                    c = 1
                    break

            elif ((x2+y2) >= 2.25):
                temp = 0
                break

            else:
                temp = 0

        if c == 1:
            notify()
            print("TYPE: Rollover")

        else:
            severityHelper(fs, len1, acc_x, acc_y)

if __name__ == '__main__':
    main()
