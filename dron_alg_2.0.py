from math import atan, sin, cos, acos
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
    dron_coord[0] += x * sin(dron_degr / 180 * pi)
    dron_coord[1] += x * cos(dron_degr / 180 * pi)
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
        degr += 5
        Round(5)
        if dist == -1:
            Bypass(dron_degr, past_dist)
            return
        if past_dist > (sin(degr / 180 * pi) * dist):
            if (sin(degr / 180 * pi) * dist) - (sin(degr / 180 * pi - 5 / 180 * pi) * past_dist) > DRONW:
                Go_around(dron_degr)
                return
    Round(-1 * degr)
    degr = 0
    while degr >= -90:
        degr -= 5
        Round(-5)
        if dist == -1:
            Bypass(dron_degr, past_dist)
            return
        if past_dist > (sin(-degr / 180 * pi) * dist):
            if (sin(-degr / 180 * pi) * dist) - (sin(5 / 180 * pi - degr / 180 * pi) * past_dist) > DRONW:
                Go_around(dron_degr)
                return

def Go_around(degr):
    if degr > 0:
        Round(90 - degr)
        if dist == -1:
            # print(past_dist, degr)
            # print('GOAR1: ', (sin(degr / 180 * pi - 1 / 180 * pi) * past_dist))
            Step(abs(sin(degr / 180 * pi - 1 / 180 * pi) * past_dist) + 0.5 * DRONW)
        else:
            # print(past_dist, degr)
            # print('GOAR2: ', (sin(degr / 180 * pi - 1 / 180 * pi) * past_dist))
            Round(-90)
            Adjust()
    else:
        # print('GOAR3')
        Round(-90 - degr)
        if dist == -1:
            # print(past_dist, degr)
            # print('GOAR1: ', (sin(degr / 180 * pi - 1 / 180 * pi) * past_dist))
            Step(abs(sin(degr / 180 * pi - 1 / 180 * pi) * past_dist) + 0.5 * DRONW)
        else:
            # print(past_dist, degr)
            # print('GOAR2: ', (sin(degr / 180 * pi - 1 / 180 * pi) * past_dist))
            Round(90)
            Adjust()

def Shortest_route():
    # print('sr:', (abs(dron_coord[0] - end_coord[0])) / (abs(dron_coord[1] - end_coord[1])))
    if ((dron_coord[0] - end_coord[0]) < 0) != ((dron_coord[1] - end_coord[1]) < 0):
        return -1 * atan((abs(dron_coord[0] - end_coord[0])) / (abs(dron_coord[1] - end_coord[1]))) / pi * 180
    return atan((abs(dron_coord[0] - end_coord[0])) / (abs(dron_coord[1] - end_coord[1]))) / pi * 180

def Adjust():
    # print('Adj')
    # print('otr', dist, past_dist)
    Round(10)
    otr = (dist ** 2 + past_dist ** 2 - 2 * dist * past_dist * cos(10 / 180 * pi)) ** 0.5
    # print(otr, dist, past_dist)
    degr = 180 - acos((otr ** 2 + past_dist ** 2 - dist ** 2) / (2 * otr * past_dist)) / pi * 180
    # print(degr)
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

def Bypass(degr, rasst):
    if degr > 0:
        Round(90-degr)
        if dist == -1:
            Step(abs(sin(degr/180*pi-1/180*pi) * rasst)+0.5 * DRONW)
        else :
            Round(-90)
            Adjust()
    else:
        Round(-90-degr)
        if dist == -1:
            Step(abs(sin(-degr/180*pi-1/180*pi) * rasst)+0.5 * DRONW)
        else :
            Round(90)
            Adjust()

    
Round(0)
Run = True
while Run:
    while dist >= 3 or dist == -1:
        if It_is_finish():
            Run = False
            break
        Round(Shortest_route()-dron_degr)
        # if Something_is_in_the_way():
        #     break
        if dist < 3 and dist != -1:
            break
        Step(0.5)
    Look_around()