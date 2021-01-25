import numpy as np
import pandas as pd

def collision_severity(G, fs, A1, A2, B1, B2, len1, len2, d, a):

    temp1 = [0.0]*len1
    temp2 = [0.0]*len1
    temp3 = [0.0]*len1
    x18 = [0.0]*len1
    xcfc18 = [0.0]*len2
    vel = [0.0]*len2

    end1 = 0 
    end2 = 0
    i = 0
    j = 0
    
    dvx = 0.0
    dvy = 0.0

    temp1[0] = B2[0]*G[0]
    temp1[1] = B2[0]*G[1] + B2[1]*G[0] - A2[1]*temp1[0]

    for i in range(2,len1):
        temp1[i] = B2[0]*G[i] + B2[1]*G[i-1] + B2[2]*G[i-2] - A2[1]*temp1[i-1] - A2[2]*temp1[i-2]

    i = len1 - 1

    for j in range(0, len1):
        temp2[j] = temp1[i]
        i -= 1

    temp3[0] = B2[0] * temp2[0]
    temp3[1] = B2[0] * temp2[1] + B2[1] * temp2[0] - A2[1] * temp3[0]

    for i in range(2, len1):
        temp3[i] = B2[0]*temp2[i] + B2[1]*temp2[i-1] + B2[2]*temp2[i-2] - A2[1]*temp3[i-1] - A2[2]*temp3[i - 2]

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
