#include <stdio.h>
#include <conio.h>
#include <math.h>
#include <stdlib.h>

void collision_severity(float G[], float fs, float A1[3], float A2[3], float B1[3], float B2[3], int len, int len2, int d, char a);

float px = 0, dvx = 0, py = 0, dvy = 0, p = 0, dv = 0;

void main()
{
    float A1[3], B1[3], A2[3], B2[3], wa, fs; //  filter co-efficients and sampling freq
    int len = 0, len2, d;       
    // length of signals and decimation factor
    printf("Sampling Frequency(kHz): ");
    scanf("%f", &fs);

    printf("Sequence Length: ");
    scanf("%d", &len);
    // building 30Hz Low Pass filter
    wa = 0.1178 / fs;
    wa = wa + (pow(wa, 3) / 3);

    A2[0] = 1;
    A2[1] = (2 * pow(wa, 2) - 2) / (1 + 1.4142 * wa + pow(wa, 2));
    A2[2] = (pow(wa, 2) - 1.4142 * wa + 1) / (pow(wa, 2) + 1.4142 * wa + 1);
    B2[0] = pow(wa, 2) / (1 + 1.4142 * wa + pow(wa, 2));
    B2[1] = 2 * B2[0];
    B2[2] = B2[0];

    d = floor(fs);
    len2 = floor((len + d - 1) / d);
    // // fetching acceleration data from csv file
    int i, tmp = 0, c = 0, sevx = 1, sevy = 1, sev = 1, L2, L3;
    float x[len], y[len], z[len], x2, y2;
    FILE *acdata;
    acdata = fopen("recdata.csv", "r");

    for (i = 0; i < len; i++)
    {
        fscanf(acdata, "%f,%f,%f", &x[i], &y[i], &z[i]);
    }

    fclose(acdata);
    // code starts
    for (i = 0; i < len; i++)
    {
        x2 = x[i] * x[i];
        y2 = y[i] * y[i];
        if ((z[i] < 0.5 && abs(y[i]) > 0.866)) // roll over
        {
            tmp = tmp + 1;
            if (tmp == (fs * 1000 * 2))
            {
                c = 1;
                break;
            }
        }
        else if ((x2 + y2) >= 2.25) // collision
        {
            tmp = 0;
            break;
        }
        else
        {
            tmp = 0;
        }
    }
    if (c == 1)
    {
        printf("\n \nTIME: x \n");
        printf("LOCATION: x \n");
        printf("VEHICLE: x \n");
        printf("VEHICLE SPEED: x \n");
        printf("TYPE: Rollover \n");
        printf("OVERALL SEVERITY: -- \n");
        printf("SENDER: auto \n DIRECTIONAL ANALYSIS: -- \n");
    }

    else
    {
        collision_severity(x, fs, A1, A2, B1, B2, len, len2, d, 'x');
        collision_severity(y, fs, A1, A2, B1, B2, len, len2, d, 'y');
        p = sqrt(pow(px, 2) + pow(py, 2));
        dv = sqrt(pow(dvx, 2) + pow(dvy, 2));

        L2 = (abs(px) >= 5 && abs(px) <= 13) || (abs(dvx) >= 12.8 && abs(dvx) <= 22.5); // airbag deployment range for most of the vehicles
        L3 = (abs(px) > 13) || (abs(dvx) > 22.5);
        if (L3 == 1)
            sevx = 3;
        else if (L3 == 0 && L2 == 1)
            sevx = 2;
        else if (abs(px) < 3)
            sevx = 0;

        L2 = (abs(py) >= 5 && abs(py) <= 13) || (abs(dvy) >= 12.8 && abs(dvy) <= 22.5);
        L3 = (abs(py) > 13) || (abs(dvy) > 22.5);
        if (L3 == 1)
            sevy = 3;
        else if (L3 == 0 && L2 == 1)
            sevy = 2;
        else if (abs(py) < 3)
            sevy = 0;

        L2 = (p >= 5 && p <= 13) || (dv >= 12.8 && dv <= 22.5);
        L3 = (p > 13) || (dv > 22.5);
        if (L3 == 1)
            sev = 3;
        else if (L3 == 0 && L2 == 1)
            sev = 2;

        printf("\n \nTIME: x \n");
        printf("LOCATION: x \n");
        printf("VEHICLE: x \n");
        printf("VEHICLE SPEED: x \n");
        printf("TYPE: Collision \n");

        if (sev == 3)
            printf("OVERALL SEVERITY: Extreme \n");
        else if (sev == 2)
            printf("OVERALL SEVERITY: High \n");
        else
            printf("OVERALL SEVERITY: Moderate \n");
        if (sev == 1)
            printf("SENDER: User \n \n");
        else
            printf("SENDER: Auto \n \n");

        printf("*DIRECTIONAL ANALYSIS* \n");
        if (px < 0)
        {
            if (sevx == 3)
                printf("FRONT: Extreme \n");
            else if (sevx == 2)
                printf("FRONT: High \n");
            else if (sevx == 1)
                printf("FRONT: Moderate \n");
            else
                printf("FRONT: -- \n");
            printf("REAR: -- \n");
        }
        else
        {
            if (sevx == 3)
                printf("REAR: Extreme \n");
            else if (sevx == 2)
                printf("REAR: High \n");
            else if (sevx == 1)
                printf("REAR: Moderate \n");
            else
                printf("REAR: -- \n");
            printf("FRONT: -- \n");
        }
        if (py < 0)
        {
            if (sevy == 3)
                printf("SIDE(RIGHT): Extreme \n");
            else if (sevy == 2)
                printf("SIDE(RIGHT): High \n");
            else if (sevy == 1)
                printf("SIDE(RIGHT): Moderate \n");
            else
                printf("SIDE(RIGHT): -- \n");
            printf("SIDE(LEFT): -- \n");
        }
        else
        {
            if (sevy == 3)
                printf("SIDE(LEFT): Extreme \n");
            else if (sevy == 2)
                printf("SIDE(LEFT): High \n");
            else if (sevy == 1)
                printf("SIDE(LEFT): Moderate \n");
            else
                printf("SIDE(LEFT): -- \n");
            printf("SIDE(RIGHT): -- \n");
        }
    }
    getch();
}

// defining funtion to estimate collision severity

void collision_severity(float G[], float fs, float A1[3], float A2[3], float B1[3], float B2[3], int len, int len2, int d, char a)
{
    int i, j, end1, end2;
    float x18[len], xcfc18[len2], vel[len2], tmp1[len], tmp2[len], tmp3[len], chk2;

    // for cfc18 30 Hz 2-pole Butterworth Filter with Zero Phase

    tmp1[0] = B2[0] * G[0];
    tmp1[1] = B2[0] * G[1] + B2[1] * G[0] - A2[1] * tmp1[0];
    for (i = 2; i < len; i++)
    {
        tmp1[i] = B2[0] * G[i] + B2[1] * G[i - 1] + B2[2] * G[i - 2] - A2[1] * tmp1[i - 1] - A2[2] * tmp1[i - 2];
    }
    for (i = len - 1, j = 0; j < len; j++)
    {
        tmp2[j] = tmp1[i];
        i = i - 1;
    }
    tmp3[0] = B2[0] * tmp2[0];
    tmp3[1] = B2[0] * tmp2[1] + B2[1] * tmp2[0] - A2[1] * tmp3[0];
    for (i = 2; i < len; i++)
    {
        tmp3[i] = B2[0] * tmp2[i] + B2[1] * tmp2[i - 1] + B2[2] * tmp2[i - 2] - A2[1] * tmp3[i - 1] - A2[2] * tmp3[i - 2];
    }
    for (i = len - 1, j = 0; j < len; j++)
    {
        x18[j] = tmp3[i];
        i = i - 1;
    }

    // decimating
    xcfc18[0] = x18[0];
    for (i = 1; i < len2; i++)
    {
        xcfc18[i] = x18[d * i];
    }
    // computing velocity array
    vel[0] = (xcfc18[0] * 0.0098) / fs;
    for (i = 1; i < len2; i++)
    {
        vel[i] = ((xcfc18[i] * 0.0098) / fs) + vel[i - 1]; // velocity in m/s
    }
    for (i = 0; i < len2; i++)
    {
        vel[i] = vel[i] * 3.6; // converting into km/h
    }
    // finding max point
    j = 0;
    for (i = 1; i < len2; i++)
    {
        if (abs(xcfc18[i]) > abs(xcfc18[j]))
            j = i;
    }
    if (a == 'x')
    {
        px = xcfc18[j];        // j is abs value max point
        chk2 = abs(0.05 * px); // according to novel approach, 5 % of max value
    }
    else
    {
        py = xcfc18[j];
        chk2 = abs(0.05 * py);
    }
    // finding end1 point
    for (i = j; i >= 0; i--)
    {
        if (abs(xcfc18[i]) <= 1.5)
        {
            end1 = i;
            break;
        }
    }
    for (i = end1 - 1; i >= 0; i--)
    {
        if (abs(xcfc18[i]) <= 1)
        {
            end1 = i;
            break;
        }
    }
    // finding end2 point
    for (i = j; i < len2; i++)
    {
        if (abs(xcfc18[i]) <= chk2)
        {
            end2 = i;
            break;
        }
    }
    if (a == 'x')
        dvx = vel[end2] - vel[end1]; // delta-v
    else
        dvy = vel[end2] - vel[end1];
}