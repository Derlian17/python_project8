import math

DRONH = 1
DRONW = 2.5
DRONL = 3
DELAY = 200
past_dist = 0
dist = 0


def Step(x):
    with open("log.txt", "a") as file:
        file.write(f"B move({x})\n")
    Find_dist()


def Round(x):
    with open("log.txt", "a") as file:
        file.write(f"B rotate({x})\n")
    Find_dist()


def Go():
    while True:
        Round(0)
        while dist <= 4:
            Step(1)
        Look_around_quick()


def Find_dist():
    global dist
    f = True
    while f:
        with open('log.txt') as file:
            end = file.readlines()[-1]
            if end[0] == 'S':
                dist = float(end[1:])
                f = False


def Dilated_pupil():
    pass


def Look_around_quick():
    Round(60)
    kriv = dist
    if dist == -1:
        Go_around(60)
    else:
        Round(-120)
        if dist == -1:
            Go_around(-60)
        else:
            Round(60)
            Look_around()


def Look_around():
    degr = 0
    while degr <= 60:
        degr += 1
        Round(1)
        if dist > (math.sin(degr) * dist) or dist == -1:
            if (math.sin(degr) * dist) - (math.sin(degr - 1) * past_dist) > DRONW:
                Go_around(degr)
    degr = 0
    Round(-60)
    while degr >= -60:
        degr -= 1
        Round(-1)
        if dist > (math.sin(degr) * dist) or dist == -1:
            if (math.sin(degr) * dist) - (math.sin(degr - 1) * past_dist) > DRONW:
                Go_around(degr)


def Go_around(degr):
    if degr:
        Round(90 - degr)
        Step(((degr - 1) * past_dist) + 0.5 * DRONW)
        Round(-90)
        Go()
    else:
        Round(-90 - degr)
        Step(((degr - 1) * past_dist) + 0.5 * DRONW)
        Round(90)
        Go()


Go()