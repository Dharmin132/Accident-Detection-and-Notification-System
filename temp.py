import pandas as pd
import math as m

def collision_severity(G, fs, A1, B1, len1, len2, d, a):

    temp1 = [0.0]*len1
    temp2 = [0.0]*len1
    temp3 = [0.0]*len1
    x18 = [0.0]*len1
    xcfc18 = [0.0]*len2
    vel = [0.0]*len2

    end1 = 0
    end2 = 0

    temp1[0] = B1[0]*G[0]
    temp1[1] = B1[0]*G[1] + B1[1]*G[0] - A1[1]*temp1[0]

    for i in range(2, len1):
        temp1[i] = B1[0]*G[i] + B1[1]*G[i-1] + B1[2]*G[i-2] - A1[1]*temp1[i-1] - A1[2]*temp1[i-2]

    # print()
    # for i in range(0, len1):
    #     print("temp1["+str(i)+"]"+str(temp1[i]))
    # print()

    i = len1 - 1

    for j in range(0, len1):
        temp2[j] = temp1[i]
        i -= 1

    temp3[0] = B1[0]*temp2[0]
    temp3[1] = B1[0]*temp2[1] + B1[1]*temp2[0] - A1[1]*temp3[0]

    for i in range(2, len1):
        temp3[i] = B1[0]*temp2[i] + B1[1]*temp2[i-1] + B1[2]*temp2[i-2] - A1[1]*temp3[i-1] - A1[2]*temp3[i - 2]

    i = len1 - 1

    for j in range(0, len1):
        x18[j] = temp3[i]
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


def main():

    dvx = 0.0
    dvy = 0.0
    px = 0.0
    py = 0.0
    p = 0.0
    dv = 0.0

    A1 = [0.0]*3
    B1 = [0.0]*3

    fs = 20
    len1 = 6601

    wa = 0.1178/fs
    wa += (wa**3)/3

    # print("wa: "+str(wa))

    A1[0] = 1
    A1[1] = (2*(wa**2) - 2)/(1 + 1.4142*wa + wa**2)
    A1[2] = (1 - 1.4142*wa + wa**2)/(1 + 1.4142*wa + wa**2)

    # print("A1[0]:"+str(A1[0]))
    # print("A1[1]:"+str(A1[1]))
    # print("A1[2]:"+str(A1[2]))

    B1[0] = (wa**2)/(1 + 1.4142*wa + wa**2)
    B1[1] = 2*B1[0]
    B1[2] = B1[0]

    # print("B1[0]:"+str(B1[0]))
    # print("B1[1]:"+str(B1[1]))
    # print("B1[2]:"+str(B1[2]))

    d = m.floor(fs)
    #print("d: "+str(d))
    len2 = m.floor((len1 + d - 1) / d)
    #print("len2: "+str(len2))

    x = [0.0]*len1
    y = [0.0]*len1
    z = [0.0]*len1

    sevx = 1
    sevy = 1
    sevz = 1

    temp = 0
    c = 0

    # reading csv file
    path = 'E:/B.Tech Project/Project Files/Accident-Detection-and-Notification-System/side07999.csv'
    data_csv = pd.read_csv(path)
    x = data_csv['x']
    y = data_csv['y']
    z = data_csv['z']

    # print()
    # print("X:")
    # print(x)

    # print()
    # print("Y:")
    # print(y)

    # print()
    # print("Z:")
    # print(z)

    # print()
    # print()

    for i in range(0, len1):

        # print("i: "+str(i))
        # print()

        x2 = x[i]**2
        y2 = y[i]**2
        # print("     x2: "+str(x2))
        # print("     y2: "+str(y2))

        if (z[i] < 0.5 and abs(y[i] > 0.866)):
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
        print("TYPE: Rollover \n")

    else:
        px, dvx = collision_severity(x, fs, A1, B1, len1, len2, d, 'x')
        py, dvy = collision_severity(y, fs, A1, B1, len1, len2, d, 'y')

        p = m.sqrt(px**2 + py**2)
        dv = m.sqrt(dvx**2 + dvy**2)

        # print()
        # print("p: "+str(p))
        # print("dv: "+str(dv))

        L2 = ((abs(px) >= 5 and abs(px) <= 13) or (abs(dvx) >= 12.8 and abs(dvx) <= 22.5))
        L3 = ((abs(px) > 13) or (abs(dvx) > 22.5))

        # print()
        # print("For X")
        # print("L2: "+str(L2))
        # print("L3: "+str(L3))

        if (L3 == 1):
            sevx = 3
        elif (L3 == 0 and L2 == 1):
            sevx = 2
        elif (abs(px) < 3):
            sevx = 0

        L2 = ((abs(py) >= 5 and abs(py) <= 13) or (abs(dvy) >= 12.8 and abs(dvy) <= 22.5))
        L3 = ((abs(py) > 13) or (abs(dvy) > 22.5))

        # print()
        # print("For Y")
        # print("L2: "+str(L2))
        # print("L3: "+str(L3))

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

        # print()
        # print("sevx: "+str(sevx))
        # print("sevy: "+str(sevy))
        # print("sevz: "+str(sevz))
        # print()

        print("TYPE: Collision \n")

        if sevz == 3:
            print("OVERALL SEVERITY: Extreme \n")
        elif sevz == 2:
            print("OVERALL SEVERITY: High \n")
        else:
            print("OVERALL SEVERITY: Moderate \n")

        if sevz == 1:
            print("SENDER: User \n \n")
        else:
            print("SENDER: Auto \n \n")

        print("*DIRECTIONAL ANALYSIS* \n")

        print()
        print("px: "+str(px))
        print("py: "+str(py))
        print()

        if px < 0:
            if sevx == 3:
                print("FRONT: Extreme \n")
            elif sevx == 2:
                print("FRONT: High \n")
            elif sevx == 1:
                print("FRONT: Moderate \n")
            else:
                print("FRONT: -- \n")

            print("REAR: -- \n")

        else:
            if sevx == 3:
                print("REAR: Extreme \n")
            elif sevx == 2:
                print("REAR: High \n")
            elif sevx == 1:
                print("REAR: Moderate \n")
            else:
                print("REAR: -- \n")

            print("FRONT: -- \n")

        if py < 0:
            if sevy == 3:
                print("SIDE(RIGHT): Extreme \n")
            elif sevy == 2:
                print("SIDE(RIGHT): High \n")
            elif sevy == 1:
                print("SIDE(RIGHT): Moderate \n")
            else:
                print("SIDE(RIGHT): -- \n")

            print("SIDE(LEFT): -- \n")

        else:
            if sevy == 3:
                print("SIDE(LEFT): Extreme \n")
            elif sevy == 2:
                print("SIDE(LEFT): High \n")
            elif sevy == 1:
                print("SIDE(LEFT): Moderate \n")
            else:
                print("SIDE(LEFT): -- \n")

            print("SIDE(RIGHT): -- \n")


if __name__ == '__main__':
    main()
