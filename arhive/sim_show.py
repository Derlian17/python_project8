#                                                 система раскомментировки
# символ #! - важное место
# символ #@! - временное решение
# символ #$ - мат. формула
# символ #!! - очень важное место
# символ #.!Error - место возможной ошибки
# символ #./ - место чтения из файла

from tkinter import *
from tkinter.filedialog import askopenfilename

from math import *
import time

from PIL import Image, ImageTk

master = Tk()
map_canvas = Canvas(master=master, width=600, height=600, background='DarkGrey')
FILE = askopenfilename()
FILE = open(FILE)
data = FILE.readlines()

Masshtabe = 20  # 100 px = 1 m

Step = 0.01

DRONEX, DRONEY, DRONEZ = eval(data[0].split(':')[1]), eval(data[1].split(':')[1]), 0  # !

DIRECTION_XY, DIRECTION_YZ = 0, 0

# XY 0 +Y, 180 -Y, 90 +X, 270 -X
# YZ 0 +Y, 180 -Y, 90 +Z, 270 -Z

DRONE_SENSORS = [(0, 0,      5, 6)]

OBJECTS = []


stDMX = 0
stDMY = 0

DXM = 0
DYM = 0

for i in data[3:]:
    if i == '\n':
        pass
    else:
        els = i.split()
        els = [els[0]] + ' '.join(els[1:]).split('_')
        els[1] = eval(els[1])
        if len(els) < 4:
            els += ['0']
        if len(els) < 4:
            els += ['0']
        els[2] = int(els[2])
        els[3] = int(els[3])
        OBJECTS.append(els)


def read():
    with open('log.txt') as file:
        end = file.readlines()[-1]
        if end[0] == 'B':
            exec(end[2:])
    if end[0] == 'B':
        with open('log.txt', 'a') as filew:
            print('\nS', *write(), file=filew)


def move(metres):
    global DRONEX, DRONEY, DRONEZ
    for s in range(round(metres / Step)):
        DRONEX += 1 * Step * sin(DIRECTION_XY / 180 * pi)
        DRONEY += 1 * Step * cos(DIRECTION_XY / 180 * pi)
        for i in OBJECTS:
            tp, cx, cy, cz, wd, hd, dh = i
            if tp == 'rect':
                if cx - wd / 2 <= DRONEX <= cx + wd / 2:
                    if cy - hd / 2 <= DRONEY <= cy + hd / 2:
                        master.destroy()
                        with open('log.txt', 'a') as filew:
                            print('\nS', 'DESTROY', file=filew)
            elif tp == 'oval':
                if (DRONEX - cx) ** 2 / wd * 2 + (DRONEY - cy) ** 2 / hd * 2 <= 1:
                    master.destroy()
                    with open('log.txt', 'a') as filew:
                        print('\nS', 'DESTROY', file=filew)
    for s in range(round(-metres / Step)):
        DRONEX -= 1 * Step * sin(DIRECTION_XY / 180 * pi)
        DRONEY -= 1 * Step * cos(DIRECTION_XY / 180 * pi)
        for i in OBJECTS:
            tp, cx, cy, cz, wd, hd, dh = i
            if tp == 'rect':
                if cx - wd / 2 <= DRONEX <= cx + wd / 2:
                    if cy - hd / 2 <= DRONEY <= cy + hd / 2:
                        master.destroy()
                        with open('log.txt', 'a') as filew:
                            print('\nS', 'DESTROY', file=filew)
            elif tp == 'oval':
                if (DRONEX - cx) ** 2 / wd * 2 + (DRONEY - cy) ** 2 / hd * 2 <= 1:
                    master.destroy()
                    with open('log.txt', 'a') as filew:
                        print('\nS', 'DESTROY', file=filew)


def rotate(angle):
    global DIRECTION_XY
    DIRECTION_XY += angle
    DIRECTION_XY %= 360


def write():
    metres_res = []

    for el in DRONE_SENSORS:
        xyd, yzd, max_len, angle_range = el
        xyd += DIRECTION_XY
        minD = -1
        for s in range(round(max_len / Step)):
            for ang in range(-round(angle_range/2), round(angle_range/2)+1):
                x = DRONEX + s * Step * sin(DIRECTION_XY / 180 * pi + ang / 180 * pi)
                y = DRONEY + s * Step * cos(DIRECTION_XY / 180 * pi + ang / 180 * pi)
                for i in OBJECTS:
                    tp, i, dxy, dyz = i
                    cx, cy, cz, wd, hd, dh = i
                    if tp == 'rect':
                        p1 = (cx - wd / 2, cy + hd / 2)
                        p2 = (cx + wd / 2, cy + hd / 2)
                        p3 = (cx + wd / 2, cy - hd / 2)
                        p4 = (cx - wd / 2, cy - hd / 2)

                        def pereschet(point, angle):
                            chetvert = ''
                            x0, y0 = point
                            dx, dy = x0 - cx, y0-cy
                            if x0 > cx and y0 >= cy:
                                chetvert = 'I'
                            elif x0 > cx and y0 < cy:
                                chetvert = 'IV'
                            elif y0 >= cy:
                                chetvert = 'II'
                            else:
                                chetvert = 'III'

                            angle_f = atan((y0 - cy) / (x0 - cx))
                            if chetvert in ['I', 'IV']:
                                pass
                            else:
                                angle_f = angle_f + pi

                            ln = (dx ** 2 + dy ** 2) ** 0.5

                            xn = cx + ln * cos(angle_f + angle)
                            yn = cy + ln * sin(angle_f + angle)

                            return xn, yn

                        def is_in_(xp, yp, pnt1, pnt2):
                            x1, y1 = pnt1
                            x2, y2 = pnt2
                            D = (x2 - x1) * (yp - y1) - (xp - x1) * (y2 - y1)
                            return D >= 0

                        p1 = pereschet(p1, dxy / 180 * pi)
                        p2 = pereschet(p2, dxy / 180 * pi)
                        p3 = pereschet(p3, dxy / 180 * pi)
                        p4 = pereschet(p4, dxy / 180 * pi)

                        f = True
                        for k in [(p1, p2), (p2, p3), (p3, p4), (p4, p1)]:
                            f = f and is_in_(x, y, *k)
                            if not f:
                                break
                        if f:
                            minD = s * Step
                            break
                        # if cx - wd / 2 <= x <= cx + wd / 2:
                        #     if cy - hd / 2 <= y <= cy + hd / 2:
                        #         if minD == -1:
                        #             minD = s * Step
                        #             break
                    elif tp == 'oval':
                        a, b = wd / 2, hd / 2
                        if (x - cx) ** 2 / wd * 2 + (y - cy) ** 2 / hd * 2 \
                                - 2 * (x - cx) * (y - cy) / a / b * cos(dxy/180*pi) <= sin(dxy / 180 * pi) ** 2:
                            minD = s * Step
                            break
                if minD == s:
                    break
            if minD == s:
                break

        metres_res.append(minD)

    return metres_res


start_time = time.monotonic()
step_time = 0.1
map_canvas.pack()


def reset_masshtabe(*args):
    global Masshtabe
    Masshtabe = round(10 ** scale.get())


scale = Scale(master, from_=0.5, to=3, command=reset_masshtabe, orient='horizontal', length=200, resolution=0.05)
scale.set(log10(20))
scale.place_configure(x=400, y=5)


def stMove_map(event):
    global stDMX, stDMY
    stDMX, stDMY = event.x / Masshtabe, event.y / Masshtabe

def Move_map(event):
    global DXM, DYM, stDMX, stDMY
    DXM += event.x / Masshtabe - stDMX
    DYM += event.y / Masshtabe - stDMY
    stDMX, stDMY = event.x/Masshtabe, event.y/Masshtabe

def restMapD(event):
    global DXM, DYM
    DXM, DYM = 0, 0


master.bind('<ButtonPress 1>', stMove_map)
master.bind('<B1-Motion>', Move_map)
master.bind('<ButtonPress 3>', restMapD)


def scale2(event):
    ins = scale.get()
    ins += event.delta / 120 * 0.05
    ins = max(0.5, min(ins, 3))
    scale.set(ins)


master.bind('<MouseWheel>', scale2)


while True:

    map_canvas.delete('map')

    if scale.get() >= 1:
        DRONEX -= DXM
        DRONEY -= DYM
        for i in range(300, -Masshtabe, -Masshtabe):
            if (i + DRONEY * Masshtabe - 300) // Masshtabe % 10 == 0:
                map_canvas.create_line(0, i - DRONEY * Masshtabe % Masshtabe,
                                       600, i - DRONEY * Masshtabe % Masshtabe, tags=['map'], width=2, stipple='gray50')
            else:
                st = 'gray50'
                map_canvas.create_line(0, i-DRONEY * Masshtabe % Masshtabe,
                                       600, i-DRONEY * Masshtabe % Masshtabe, tags=['map'], stipple=st)
            if (i + DRONEX * Masshtabe - 300) // Masshtabe % 10 == 0:
                map_canvas.create_line(i - DRONEX * Masshtabe % Masshtabe, 0,
                                       i - DRONEX * Masshtabe % Masshtabe, 600, tags=['map'], width=2, stipple='gray50')
            else:
                st = 'gray50'
                map_canvas.create_line(i-DRONEX * Masshtabe % Masshtabe, 0,
                                       i-DRONEX * Masshtabe % Masshtabe, 600, tags=['map'], stipple=st)
        for i in range(300, 600+Masshtabe, Masshtabe):
            if (i + DRONEY * Masshtabe - 300) // Masshtabe % 10 == 0:
                map_canvas.create_line(0, i - DRONEY * Masshtabe % Masshtabe,
                                       600, i - DRONEY * Masshtabe % Masshtabe, tags=['map'], width=2, stipple='gray50')
            else:
                st = 'gray50'
                map_canvas.create_line(0, i-DRONEY * Masshtabe % Masshtabe,
                                       600, i-DRONEY * Masshtabe % Masshtabe, tags=['map'], stipple=st)
            if (i + DRONEX * Masshtabe - 300) // Masshtabe % 10 == 0:
                map_canvas.create_line(i - DRONEX * Masshtabe % Masshtabe, 0,
                                       i - DRONEX * Masshtabe % Masshtabe, 600, tags=['map'], width=2, stipple='gray50')
            else:
                st = 'gray50'
                map_canvas.create_line(i-DRONEX * Masshtabe % Masshtabe, 0,
                                       i-DRONEX * Masshtabe % Masshtabe, 600, tags=['map'], stipple=st)
        DRONEX += DXM
        DRONEY += DYM
    else:
        DRONEX -= DXM
        DRONEY -= DYM
        for i in range(300, -10*Masshtabe, -10*Masshtabe):
            map_canvas.create_line(0, i - DRONEY * Masshtabe % (10 * Masshtabe),
                                   600, i - DRONEY * Masshtabe % (10 * Masshtabe), tags=['map'], width=2, stipple='gray50')
            map_canvas.create_line(i - DRONEX * Masshtabe % (10 * Masshtabe), 0,
                                   i - DRONEX * Masshtabe % (10 * Masshtabe), 600, tags=['map'], width=2, stipple='gray50')

        for i in range(300, 600+10*Masshtabe, 10*Masshtabe):
            map_canvas.create_line(0, i - DRONEY * Masshtabe % (10 * Masshtabe),
                                   600, i - DRONEY * Masshtabe % (10 * Masshtabe), tags=['map'], width=2, stipple='gray50')
            map_canvas.create_line(i - DRONEX * Masshtabe % (10 * Masshtabe), 0,
                                   i - DRONEX * Masshtabe % (10 * Masshtabe), 600, tags=['map'], width=2, stipple='gray50')
        DRONEX += DXM
        DRONEY += DYM
    for i in OBJECTS:
        tp, i, dxy, dyz = i
        cx, cy, cz, wd, hd, dh = i
        cx *= Masshtabe
        cy *= Masshtabe
        wd *= Masshtabe
        hd *= Masshtabe
        if tp == 'oval':
            points = []
            a, b = wd / 2, hd / 2
            for ang in range(0, 360, 10):
                x0, y0 = a * cos(ang / 180 * pi), b * sin(ang / 180 * pi)
                x1 = x0 * cos(dxy / 180 * pi) - y0 * sin(dxy / 180 * pi)
                y1 = x0 * sin(dxy / 180 * pi) + y0 * cos(dxy / 180 * pi)
                points.append(x1+cx)
                points.append(y1+cy)

            map_canvas.create_polygon(*points, fill='grey', tags=['map', 'move', 'obj'])

            # map_canvas.create_oval(cx-wd/2, cy-hd/2, cx+wd/2, cy+hd/2, fill='grey',
            #                        tags=['map', 'move'])
        if tp == 'rect':
            p1 = (cx - wd / 2, cy + hd / 2)
            p2 = (cx + wd / 2, cy + hd / 2)
            p3 = (cx + wd / 2, cy - hd / 2)
            p4 = (cx - wd / 2, cy - hd / 2)

            def pereschet(point, angle):
                chetvert = ''
                x0, y0 = point
                dx, dy = x0 - cx, y0 - cy
                if x0 >= cx and y0 >= cy:
                    chetvert = 'I'
                elif x0 >= cx and y0 < cy:
                    chetvert = 'IV'
                elif y0 >= cy:
                    chetvert = 'II'
                else:
                    chetvert = 'III'

                angle_f = atan((y0 - cy) / (x0 - cx))
                if chetvert in ['I', 'IV']:
                    pass
                else:
                    angle_f = angle_f + pi

                ln = (dx ** 2 + dy ** 2) ** 0.5

                xn = cx + ln * cos(angle_f + angle)
                yn = cy + ln * sin(angle_f + angle)

                return xn, yn


            p1 = pereschet(p1, dxy / 180 * pi)
            p2 = pereschet(p2, dxy / 180 * pi)
            p3 = pereschet(p3, dxy / 180 * pi)
            p4 = pereschet(p4, dxy / 180 * pi)

            map_canvas.create_polygon(*p1, *p2, *p3, *p4, fill='grey',
                                        tags=['map', 'move', 'obj'])

    map_canvas.move('move', 300-DRONEX*Masshtabe, 300-DRONEY*Masshtabe)

    for sens in DRONE_SENSORS:
        xy, _, dst, ang_range = sens
        dst *= Masshtabe
        map_canvas.create_arc(300-dst, 300-dst, 300+dst, 300+dst, start=DIRECTION_XY+xy-ang_range/2-90,
                              extent=ang_range, tags=['map', 'obj'])

    img = Image.open('img.png')
    img = img.resize((round(1.5 * Masshtabe), round(1.5 * Masshtabe)))
    img = img.rotate(DIRECTION_XY, expand=True)
    img = ImageTk.PhotoImage(img)
    # map_canvas.create_oval(300-0.2*Masshtabe, 300-0.2*Masshtabe, 300+0.2*Masshtabe, 300+0.2*Masshtabe,
    #                             fill='red', tags=['map'])
    # map_canvas.create_line(300-0.5*Masshtabe*sin(DIRECTION_XY / 180 * pi+ pi),
    #                        300-0.5*Masshtabe*cos(DIRECTION_XY / 180 * pi+ pi), 300, 300, tags=['map'], fill='red',
    #                        width=2)
    map_canvas.create_image(300, 300, image=img, tags=['map', 'obj'])
    map_canvas.move('obj', DXM*Masshtabe, DYM*Masshtabe)
    master.update()
    read()

    time.sleep(step_time - ((time.monotonic() - start_time) % step_time))


