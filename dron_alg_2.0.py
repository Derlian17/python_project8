import math
from math import pi

DRONH = 1
DRONW = 2.5
DRONL = 3

dron_coord = [0, 0, 0]
end_coord = [0, 70, 0]
dron_degr = 0
past_dist = 0
dist = 0

def Step(x):
    dron_coord[0] += x * math.sin(dron_degr / 180 * pi)
    dron_coord[1] += x * math.cos(dron_degr / 180 * pi)
    with open("log.txt", "a") as file:
        file.write(f"B move({x})\n")
    Find_dist()

def Round(x):
    global dron_degr
    dron_degr += x
    with open("log.txt", "a") as file:
        file.write(f"B rotate({x})\n")
    Find_dist()

def Find_dist():
    global past_dist
    global dist
    past_dist = dist
    f = True
    while f:
        with open('log.txt') as file:
            end = file.readlines()[-1]
            if end[0] == 'S':
                dist = float(end[1:])
                f = False

def Something_is_in_the_way():
    Round(5)
    Round(-10)
    if dist == -1 or past_dist == -1:
        Round(5)
        return 0
    else:
        Round(5)
        return 1

def Look_around():
    degr = 0
    while degr <= 90:
        degr += 1
        Round(1)
        if dist == -1:
            Go_around(degr)
        if dist > (math.sin(degr / 180 * pi) * dist):
            if (math.sin(degr / 180 * pi) * dist) - (math.sin(degr / 180 * pi - 1 / 180 * pi) * past_dist) > DRONW:
                Go_around(degr)
                return
    Round(-1 * degr)
    degr = 0
    while degr >= -90:
        degr -= 1
        Round(-1)
        if dist == -1:
            Go_around(degr)
        if dist > (math.sin(-degr / 180 * pi) * dist):
            if (math.sin(-degr / 180 * pi) * dist) - (math.sin(1 * pi / 180 - degr / 180 * pi) * past_dist) > DRONW:
                Go_around(degr)
                return

def Go_around(degr):
    if degr:
        Round(90 - degr)
        if dist == -1:
            Step((math.sin(degr / 180 * pi - 1 / 180 * pi) * past_dist) + 0.5 * DRONW)
        else:
            Round(-90)
            Adjust()
    else:
        Round(-90 - degr)
        Step(((degr - 1) * past_dist) + 0.5 * DRONW)
        Round(90)

def Shortest_route():
    if (dron_coord[0] - end_coord[0]) < 0 or (dron_coord[1] - end_coord[1]) < 0:
        return -1 * math.atan((abs(dron_coord[0] - end_coord[0])) / (abs(dron_coord[1] - end_coord[1]))) / pi * 180
    return math.atan((abs(dron_coord[0] - end_coord[0])) / (abs(dron_coord[1] - end_coord[1]))) / pi * 180

def Adjust():
    otr = math.sqrt((dist * dist) + (past_dist * past_dist) - 2 * dist * past_dist * math.cos(10 / 180 * pi))
    degr = 180 - (math.acos(((otr * otr) + (past_dist * past_dist) - (dist * dist)) / (2 * otr * past_dist))) / pi * 180
    if dist <= past_dist:
        degr = degr * (-1)
    Round(-10)
    while dist != -1 or dist <= 4:
        Round(degr)
        Step(0.5)
        Round(-degr)

def It_is_finish():
    if (abs(dron_coord[0] - end_coord[0]) <= 2) and (abs(dron_coord[1] - end_coord[1]) <= 2) and (abs(dron_coord[2] - end_coord[2]) <= 2):
        return 1
    else:
        return 0
    
Round(0)
Run = True
while Run:
    while dist >= 3:
        if It_is_finish():
            Run = False
            break
        Round(Shortest_route())
        if Something_is_in_the_way():
            break
        Step(0.5)
    Look_around()