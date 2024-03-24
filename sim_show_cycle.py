#                                                 система раскомментировки
# символ #! - важное место
# символ #@! - временное решение
# символ #$ - мат. формула
# символ #!! - очень важное место
# символ #.!Error - место возможной ошибки
# символ #./ - место чтения из файла
# символ ##/ - место создания важной переменной

from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.font import Font

from math import *
import time

from PIL import Image, ImageTk

from datetime import timedelta

master = Tk()
map_canvas = Canvas(master=master, width=600, height=600, background='DarkGrey')
import os
Path = askdirectory()
FILES = []
for _, _, files in os.walk(Path):
    FILES = files
    break


if True:
    Masshtabe = 20  # Masshtabe px = 1 m    ##/

    Step = 0.01  # ##/ минимальный шаг (в метрах)
    DIRECTION_XY, DIRECTION_YZ = 0, 0  # ##/ #@!
    #                                   первая переменная определяет поворот в плоскости XOY,
    #                                   вторая в плоскости YOZ, Y-ось сонаправлена с полетом дрона. временно неактивна

    # XY 0 +Y, 180 -Y, 90 +X, 270 -X
    # YZ 0 +Y, 180 -Y, 90 +Z, 270 -Z

    DRONE_SENSORS = [(0, 0, 5.1, 6)]  # ##/
    #                                    первая переменная в кортеже определяет угол в пл. XOY,
    #                                    вторая - в YOZ, третья обозначает расстояние на котором
    #                                    сканер засекает объект, четвертая - угол на который расходятся лучи.
    #                                    !!! ВНИМАНИЕ !!! С УВЕЛИЧЕНИЕМ УГЛА ИЛИ РАССТОЯНИЯ ВЫЧИСЛЕНИЯ
    #                                    ПРОПОРЦИОНАЛЬНО РАСТУТ !!!

    OBJECTS = []  # переменная для объектов карты  ##/

    stDMX = 0  # переменные для движения карты
    stDMY = 0  #

    DXM = 0  #
    DYM = 0  #

    DX, DY = 0, 0

    DESTROY = False  # переменная на прекращение цикла

    SUBPOINTS = [(0, 0, 0), (0.5, 0.42, 0), (0.5, -0.42, 0), (-0.5, 0.42, 0), (-0.5, -0.42, 0)]

    Max_speed = 5
    Max_rot_speed = 5 * (pi * 1) / 360

    now_speed = 4
    now_rot_speed = 2 / (pi * 0.5 * 2) * 360

    move_step = 20
    rot_step = 20

    Angle_step = 1

start_time = time.time()


def set_constants():
    global Masshtabe, Step, DIRECTION_XY, DIRECTION_YZ, DRONE_SENSORS, OBJECTS
    global stDMX, stDMY, DXM, DYM, DX, DY, DESTROY, SUBPOINTS, Max_speed, now_speed
    global Max_rot_speed, now_rot_speed, move_step, rot_step, Angle_step
    Masshtabe = 20  # Masshtabe px = 1 m    ##/

    Step = 0.01  # ##/ минимальный шаг (в метрах)
    DIRECTION_XY, DIRECTION_YZ = 0, 0  # ##/ #@!
    #                                   первая переменная определяет поворот в плоскости XOY,
    #                                   вторая в плоскости YOZ, Y-ось сонаправлена с полетом дрона. временно неактивна

    # XY 0 +Y, 180 -Y, 90 +X, 270 -X
    # YZ 0 +Y, 180 -Y, 90 +Z, 270 -Z

    DRONE_SENSORS = [(0, 0, 5.1, 6)]  # ##/
    #                                    первая переменная в кортеже определяет угол в пл. XOY,
    #                                    вторая - в YOZ, третья обозначает расстояние на котором
    #                                    сканер засекает объект, четвертая - угол на который расходятся лучи.
    #                                    !!! ВНИМАНИЕ !!! С УВЕЛИЧЕНИЕМ УГЛА ИЛИ РАССТОЯНИЯ ВЫЧИСЛЕНИЯ
    #                                    ПРОПОРЦИОНАЛЬНО РАСТУТ !!!

    OBJECTS = []  # переменная для объектов карты  ##/

    stDMX = 0  # переменные для движения карты
    stDMY = 0  #

    DXM = 0  #
    DYM = 0  #

    DX, DY = 0, 0

    DESTROY = False  # переменная на прекращение цикла

    SUBPOINTS = [(0, 0, 0), (0.5, 0.42, 0), (0.5, -0.42, 0), (-0.5, 0.42, 0), (-0.5, -0.42, 0)]

    Max_speed = 5
    Max_rot_speed = 5 * (pi * 1) / 360

    now_speed = 4
    now_rot_speed = 2 / (pi * 0.5 * 2) * 360

    move_step = 20
    rot_step = 20

    Angle_step = 1


def file_read():
    global DRONEX, DRONEY, DRONEZ
    DRONEX, DRONEY, DRONEZ = eval(data[0].split(':')[1]), eval(data[1].split(':')[1]), 0  # #@! #./
    for i in data[3:]:
        if i.strip() in ['\n', '']:
            pass
        else:
            els = i.split()
            els = [els[0]] + ' '.join(els[1:]).split('_')
            els[1] = eval(els[1])
            if len(els) < 4:
                els += ['0']
            if len(els) < 4:
                els += ['0']
            els[2] = float(els[2])
            els[3] = float(els[3])
            OBJECTS.append(els)  # заполнение переменной объектами


def main():
    global start_time, rotate, move, Finish, set_ang

    def read():
        with open('log.txt') as file:
            end = file.readlines()[-1]  # #.!Error считывание строк из файла. !! !!! !!! #./
            #
            #
            #               Буду благодарен, если кто-нибудь объяснит, почему ломается, если в конце файла нет переноса строки
            #
            #
            if end[0] == 'B':
                exec(end[2:])  # #! считывание команды из последней строки
        if end[0] == 'B' and DESTROY is False:
            with open('log.txt', 'a') as filew:
                print('\nS', *write(), file=filew)  # #! ввод в файл показаний датчиков !! \n - перенос строки

    def Is_Destroy():
        global DESTROY
        for dp in SUBPOINTS:
            dx0, dy0, dz0 = dp

            def pereschet0(point, angle):
                try:
                    chetvert = ''
                    x0, y0 = point
                    cx, cy = 0, 0
                    dx, dy = x0 - cx, y0 - cy
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
                except ZeroDivisionError:
                    return point

            pnt = (dx0, dy0)
            pnt = pereschet0(pnt, DIRECTION_XY)

            x, y = DRONEX + pnt[0], DRONEY + pnt[1]

            for i in OBJECTS:
                obj = i.copy()
                tp, i, dxy, dyz = i
                cx, cy, cz, wd, hd, dh = i
                if tp == 'rect':
                    p1 = (cx - wd / 2 - Step, cy + hd / 2 + Step)  # #$ начало определения принадлежности точки
                    #                                                                       прямоугольнику повернутому
                    #                                                   на некий угол 😔
                    p2 = (cx + wd / 2 + Step, cy + hd / 2 + Step)
                    p3 = (cx + wd / 2 + Step, cy - hd / 2 - Step)
                    p4 = (cx - wd / 2 - Step, cy - hd / 2 - Step)

                    def pereschet(point, angle):
                        chetvert = ''
                        x0, y0 = point
                        dx, dy = x0 - cx, y0 - cy
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
                        return D <= 0

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
                        DESTROY = True
                        with open('log.txt', 'a') as filew:
                            print('\nS', 'DESTROY', file=filew)  # #! операция записи в файл факта уничтожения
                        return
                elif tp == 'oval':
                    a, b = wd / 2, hd / 2  # #$ мат. формула для овала
                    if (((x - cx) * cos(dxy / 180 * pi) + (y - cy) * sin(dxy / 180 * pi)) ** 2) / (a ** 2) \
                            + (((x - cx) * sin(dxy / 180 * pi) - (y - cy) * cos(dxy / 180 * pi)) ** 2) / (b ** 2) <= 1:
                        DESTROY = True
                        with open('log.txt', 'a') as filew:
                            print('\nS', 'DESTROY', file=filew)
                        return

    def move(metres):
        global DRONEX, DRONEY, DRONEZ, DESTROY
        st_time = time.time()
        for s in range(round(metres / Step)):
            DRONEX += 1 * Step * sin(DIRECTION_XY / 180 * pi)
            DRONEY += 1 * Step * cos(DIRECTION_XY / 180 * pi)
            Is_Destroy()
            if s % move_step == 0:
                update()
                lst_time = st_time
                time.sleep(max(-time.time() + lst_time + move_step * Step / now_speed, 0))
                st_time = time.time()
        st_time = time.time()
        for s in range(round(-metres / Step)):  # f ntgthm ltnbirb bltv yfpfl
            DRONEX -= 1 * Step * sin(DIRECTION_XY / 180 * pi)
            DRONEY -= 1 * Step * cos(DIRECTION_XY / 180 * pi)
            Is_Destroy()
            if s % move_step == 0:
                update()
                lst_time = st_time
                time.sleep(max(-time.time() + lst_time + move_step * Step / now_speed, 0))
                st_time = time.time()

    def rotate(angle):
        global DIRECTION_XY
        st_time = time.time()
        for d in range(round(angle / Angle_step)):
            DIRECTION_XY += 1 * Angle_step
            Is_Destroy()
            if d % rot_step == 0:
                update()
                lst_time = st_time
                time.sleep(max(-time.time() + lst_time + rot_step * Angle_step / now_rot_speed, 0))
                st_time = time.time()
        st_time = time.time()
        for d in range(round(-angle / Angle_step)):
            DIRECTION_XY -= 1 * Angle_step
            Is_Destroy()
            if d % rot_step == 0:
                update()
                lst_time = st_time
                time.sleep(max(-time.time() + lst_time + rot_step * Angle_step / now_rot_speed, 0))
                st_time = time.time()
        # DIRECTION_XY += angle
        DIRECTION_XY %= 360
        Is_Destroy()

    def set_ang(angle):
        global DIRECTION_XY
        DIRECTION_XY = angle
        DIRECTION_XY %= 360
        Is_Destroy()

    def Finish():
        raise ImportError('WIN!!!')

    def write():  # yt ktpmnt? jyj dfc cj;htn...
        metres_res = []

        for el in DRONE_SENSORS:
            xyd, yzd, max_len, angle_range = el
            xyd += DIRECTION_XY
            minD = -1
            for s in range(round(max_len / Step) + 1):
                for ang in range(-round(angle_range / 2), round(angle_range / 2) + 1):
                    x = DRONEX + s * Step * sin(DIRECTION_XY / 180 * pi + ang / 180 * pi)
                    y = DRONEY + s * Step * cos(DIRECTION_XY / 180 * pi + ang / 180 * pi)
                    for i in OBJECTS:
                        obj = i.copy()
                        tp, i, dxy, dyz = i
                        cx, cy, cz, wd, hd, dh = i
                        if tp == 'rect':
                            p1 = (cx - wd / 2 - Step, cy + hd / 2 + Step)  # #$ см выше
                            p2 = (cx + wd / 2 + Step, cy + hd / 2 + Step)
                            p3 = (cx + wd / 2 + Step, cy - hd / 2 - Step)
                            p4 = (cx - wd / 2 - Step, cy - hd / 2 - Step)

                            def pereschet(point, angle):
                                chetvert = ''
                                x0, y0 = point
                                dx, dy = x0 - cx, y0 - cy
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
                                return D <= 0

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
                            a, b = wd / 2, hd / 2  # #$
                            if (((x - cx) * cos(dxy / 180 * pi) + (y - cy) * sin(dxy / 180 * pi)) ** 2) / (a ** 2) \
                                    + (((x - cx) * sin(dxy / 180 * pi) - (y - cy) * cos(dxy / 180 * pi)) ** 2) / (
                                    b ** 2) <= 1:
                                minD = s * Step
                                break
                    if minD == s * Step:
                        break
                if minD == s * Step:
                    break

            metres_res.append(minD)

        return metres_res

    # #!  ЗДЕСЬ НАЧИНАЕТСЯ  М̶о̶р̶д̶о̶р̶  часть вызова read() и графической обработки
    #                                                   интересно с чего вдруг воскл знак стал курсивом?
    start_time = time.monotonic()
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
        stDMX, stDMY = event.x / Masshtabe, event.y / Masshtabe

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

    def move2up(event):
        if DESTROY is False:
            move(10 * Step)

    def move2down(event):
        if DESTROY is False:
            move(-10 * Step)

    def move2right(event):
        if DESTROY is False:
            rotate(5)

    def move2left(event):
        if DESTROY is False:
            rotate(-5)

    master.bind('<Key-Up>', move2up)
    master.bind('<Key-Down>', move2down)
    master.bind('<Key-Left>', move2left)
    master.bind('<Key-Right>', move2right)

    SensUPDATE = False
    sensors = map_canvas.create_text(10, 10, text='', anchor='nw', fill='green', font=Font(size=18, weight='bold'))

    def show_and_dont_hide(event):
        global SensUPDATE
        SensUPDATE = True

    master.bind('<Key-Tab>', show_and_dont_hide)

    def but2(event):
        global DIRECTION_XY, DX, DY
        show_and_dont_hide('')
        DX, DY = DRONEX, DRONEY
        x, y = event.x, event.y
        x, y = (x - 300) / Masshtabe - DXM, (y - 300) / Masshtabe - DYM
        ln = (x ** 2 + y ** 2) ** 0.5
        x0, y0 = x, y

        if x0 > 0 and y0 >= 0:
            chetvert = 'I'
        elif x0 > 0 and y0 < 0:
            chetvert = 'IV'
        elif y0 >= 0:
            chetvert = 'II'
        else:
            chetvert = 'III'

        try:
            angle_f = -atan(y0 / x0) + pi / 2 - pi
            if chetvert in ['III', 'II']:
                pass
            else:
                angle_f = angle_f + pi
        except ZeroDivisionError:
            if chetvert == 'II':
                angle_f = 0
            else:
                angle_f = -pi

        DIRECTION_XY = 0
        rotate(angle_f * 180 / pi)
        move(ln)

    master.bind('<ButtonPress 2>', but2)

    def destroy(*args):
        with open('log.txt', 'a') as file:
            print('S WindowDestroy', file=file)

    master.bind('<Destroy>', destroy)

    def update():
        global DX, DY, DRONEX, DRONEY, img
        map_canvas.delete('map')

        if scale.get() >= 1:
            DRONEX -= DXM
            DRONEY -= DYM
            for i in range(300, -Masshtabe, -Masshtabe):
                if (i + DRONEY * Masshtabe - 300) // Masshtabe % 10 == 0:
                    map_canvas.create_line(0, i - DRONEY * Masshtabe % Masshtabe,
                                           600, i - DRONEY * Masshtabe % Masshtabe, tags=['map'], width=2,
                                           stipple='gray50')
                else:
                    st = 'gray50'
                    map_canvas.create_line(0, i - DRONEY * Masshtabe % Masshtabe,
                                           600, i - DRONEY * Masshtabe % Masshtabe, tags=['map'], stipple=st)
                if (i + DRONEX * Masshtabe - 300) // Masshtabe % 10 == 0:
                    map_canvas.create_line(i - DRONEX * Masshtabe % Masshtabe, 0,
                                           i - DRONEX * Masshtabe % Masshtabe, 600, tags=['map'], width=2,
                                           stipple='gray50')
                else:
                    st = 'gray50'
                    map_canvas.create_line(i - DRONEX * Masshtabe % Masshtabe, 0,
                                           i - DRONEX * Masshtabe % Masshtabe, 600, tags=['map'], stipple=st)
            for i in range(300, 600 + Masshtabe, Masshtabe):
                if (i + DRONEY * Masshtabe - 300) // Masshtabe % 10 == 0:
                    map_canvas.create_line(0, i - DRONEY * Masshtabe % Masshtabe,
                                           600, i - DRONEY * Masshtabe % Masshtabe, tags=['map'], width=2,
                                           stipple='gray50')
                else:
                    st = 'gray50'
                    map_canvas.create_line(0, i - DRONEY * Masshtabe % Masshtabe,
                                           600, i - DRONEY * Masshtabe % Masshtabe, tags=['map'], stipple=st)
                if (i + DRONEX * Masshtabe - 300) // Masshtabe % 10 == 0:
                    map_canvas.create_line(i - DRONEX * Masshtabe % Masshtabe, 0,
                                           i - DRONEX * Masshtabe % Masshtabe, 600, tags=['map'], width=2,
                                           stipple='gray50')
                else:
                    st = 'gray50'
                    map_canvas.create_line(i - DRONEX * Masshtabe % Masshtabe, 0,
                                           i - DRONEX * Masshtabe % Masshtabe, 600, tags=['map'], stipple=st)
            DRONEX += DXM
            DRONEY += DYM
        else:
            DRONEX -= DXM
            DRONEY -= DYM
            for i in range(300, -10 * Masshtabe, -10 * Masshtabe):
                map_canvas.create_line(0, i - DRONEY * Masshtabe % (10 * Masshtabe),
                                       600, i - DRONEY * Masshtabe % (10 * Masshtabe), tags=['map'], width=2,
                                       stipple='gray50')
                map_canvas.create_line(i - DRONEX * Masshtabe % (10 * Masshtabe), 0,
                                       i - DRONEX * Masshtabe % (10 * Masshtabe), 600, tags=['map'], width=2,
                                       stipple='gray50')

            for i in range(300, 600 + 10 * Masshtabe, 10 * Masshtabe):
                map_canvas.create_line(0, i - DRONEY * Masshtabe % (10 * Masshtabe),
                                       600, i - DRONEY * Masshtabe % (10 * Masshtabe), tags=['map'], width=2,
                                       stipple='gray50')
                map_canvas.create_line(i - DRONEX * Masshtabe % (10 * Masshtabe), 0,
                                       i - DRONEX * Masshtabe % (10 * Masshtabe), 600, tags=['map'], width=2,
                                       stipple='gray50')
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
                    points.append(x1 + cx)
                    points.append(y1 + cy)

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

        map_canvas.move('move', 300 - DRONEX * Masshtabe, 300 - DRONEY * Masshtabe)

        for sens in DRONE_SENSORS:
            xy, _, dst, ang_range = sens
            dst *= Masshtabe
            map_canvas.create_arc(300 - dst, 300 - dst, 300 + dst, 300 + dst,
                                  start=DIRECTION_XY + xy - ang_range / 2 - 90,
                                  extent=ang_range, tags=['map', 'obj', 'sens'])

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

        def pereschet0(point, angle):
            try:
                chetvert = ''
                x0, y0 = point
                cx, cy = 0, 0
                dx, dy = x0 - cx, y0 - cy
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
            except ZeroDivisionError:
                return point

        for pnt in SUBPOINTS:
            dx, dy, dz = pnt
            pntn = pereschet0((dx, dy), -DIRECTION_XY / 180 * pi + pi)
            xo, yo = pntn[0] * Masshtabe + 300, pntn[1] * Masshtabe + 300
            map_canvas.create_oval(xo + 1, yo + 1, xo - 1, yo - 1,
                                   fill='green', tags=['map', 'obj'], outline='green')
        map_canvas.move('obj', DXM * Masshtabe, DYM * Masshtabe)
        if SensUPDATE:
            map_canvas.itemconfigure(sensors, text=' '.join(map(str, write())))

        map_canvas.create_text(520, 60, text=str(timedelta(seconds=round(time.monotonic() - start_time))), tags=['map'],
                               fill='green', font=Font(size=14))

        master.update()

    while DESTROY is False:
        update()
        DX, DY = DRONEX, DRONEY
        read()
    raise FileExistsError('DESTROY')


for FILE in FILES:
    try:
        set_constants()
        FILE_o = open(Path+'\\'+FILE)
        data = FILE_o.readlines()
        file_read()
        try:
            master.wm_title(FILE)
            main()
        except ImportError:
            print(FILE, 'complited', 'in a time', timedelta(seconds=time.monotonic()-start_time))
        except FileExistsError:
            print(FILE, 'failed', 'in a time', timedelta(seconds=time.monotonic()-start_time),
                  'in coords', DRONEX, ';', DRONEY)
    except TclError:
        master = Tk()
        map_canvas = Canvas(master=master, width=600, height=600, background='DarkGrey')
    except Exception:
        print(FILE, 'error_read')
