from tkinter import *
from math import *

master = Tk()
canvas = Canvas(master, width=600, height=600)

img = PhotoImage(master=master, file='img_1.png')
canvas.pack()

DRONEX, DRONEY = 0, 0

Masshtabe = 20  # Masshtabe px = 1 m    ##/

Step = 0.01  # ##/ минимальный шаг (в метрах)

DIRECTION_XY, DIRECTION_YZ = 0, 0  # ##/ #@!
#                                   первая переменная определяет поворот в плоскости XOY,
#                                   вторая в плоскости YOZ, Y-ось сонаправлена с полетом дрона. временно неактивна

# XY 0 +Y, 180 -Y, 90 +X, 270 -X
# YZ 0 +Y, 180 -Y, 90 +Z, 270 -Z

OBJECTS = []  # переменная для объектов карты  ##/


stDMX = 0  # переменные для движения карты
stDMY = 0  #

DXM = 0  #
DYM = 0  #


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
    update()


def restMapD(event):
    global DXM, DYM
    DXM, DYM = 0, 0
    update()


master.bind('<ButtonPress 3>', stMove_map)
master.bind('<B3-Motion>', Move_map)

master.bind('<Key R>', restMapD)
master.bind('<Key r>', restMapD)


def create_object(event):
    x, y = event.x, event.y
    x -= 300
    y -= 300
    itp = 'rect'
    depth = -1
    z = 0
    xy_angle = 0
    yz_angle = 0
    if 1 <= scale.get() <= 2.1:
        x, y = x - DXM * Masshtabe % Masshtabe, y - DYM * Masshtabe % Masshtabe
        x, y = round(x / Masshtabe), round(y / Masshtabe)
        x, y = x - DXM + DXM * Masshtabe % Masshtabe / Masshtabe, y - DYM + DYM * Masshtabe % Masshtabe / Masshtabe
        width, height = 4, 2
        # xa, \
        # ya = \
        #     (x + DXM) * Masshtabe + 300, \
        #     (y + DYM) * Masshtabe + 300
        # canvas.create_oval(xa-3, ya-3, xa+3, ya+3)
        # OBJECTS.append(['rect', [x, y, 0, 4, 2, -1], 45, 0])
    elif scale.get() <= 1:
        x, y = x - DXM * Masshtabe % (10 * Masshtabe), y - DYM * Masshtabe % (10 * Masshtabe)
        x, y = round(x / Masshtabe / 10), round(y / Masshtabe / 10)
        x, y = x * 10 - DXM + DXM * Masshtabe % (10 * Masshtabe) / Masshtabe, \
               y * 10 - DYM + DYM * Masshtabe % (10 * Masshtabe) / Masshtabe
        width, height = 4, 2
        # OBJECTS.append(['rect', [x, y, 0, 4, 2, -1], 45, 0])
    else:
        x, y = x - DXM * Masshtabe % (0.1 * Masshtabe), y - DYM * Masshtabe % (0.1 * Masshtabe)
        x, y = round(x / Masshtabe / 0.1), round(y / Masshtabe / 0.1)
        x, y = x * 0.1 - DXM + DXM * Masshtabe % (0.1 * Masshtabe) / Masshtabe, \
               y * 0.1 - DYM + DYM * Masshtabe % (0.1 * Masshtabe) / Masshtabe
        width, height = 0.4, 0.2
        # OBJECTS.append(['rect', [x, y, 0, 0.04, 0.02, -1], 45, 0])
    OBJECTS.append([itp, [x, y, z, width, height, depth], xy_angle, yz_angle])

    update()

    dialog = Tk()
    dialog.geometry = '160x120'
    dialog.wm_resizable(False, False)

    def iupdate(*args):
        OBJECTS[-1] = [itp_entr.get(),
                       [
                           float(x_entr.get()),
                           float(y_entr.get()),
                           float(z_entr.get()),
                           float(width_entr.get()),
                           float(height_entr.get()),
                           float(depth_entr.get())
                       ],
                       float(xy_angle_entr.get()),
                       float(yz_angle_entr.get())]
        update()

    # c = Canvas(dialog, width=400, height=200)
    # c.pack()

    itp_entr = Entry(dialog)
    itp_entr.place_configure(x=10, y=7, width=120)
    itp_entr.insert('end', itp)

    x_entr = Entry(dialog)
    x_entr.place_configure(x=10, y=30, width=50)
    x_entr.insert('end', str(x))

    y_entr = Entry(dialog)
    y_entr.place_configure(x=60, y=30, width=50)
    y_entr.insert('end', str(y))

    z_entr = Entry(dialog)
    z_entr.place_configure(x=110, y=30, width=50)
    z_entr.insert('end', str(z))
    z_entr.configure(state='disabled')

    width_entr = Entry(dialog)
    width_entr.place_configure(x=10, y=53, width=40)
    width_entr.insert('end', str(width))

    height_entr = Entry(dialog)
    height_entr.place_configure(x=60, y=53, width=40)
    height_entr.insert('end', str(height))

    depth_entr = Entry(dialog)
    depth_entr.place_configure(x=110, y=53, width=40)
    depth_entr.insert('end', str(depth))
    depth_entr.configure(state='disabled')

    # xy_degree_scale = Scale(dialog, from_=-180, to=180, length=120, orient='horizontal')
    # xy_degree_scale.place_configure(x=10, y=70, width=360)
    # xy_degree_scale.set(xy_angle)

    xy_angle_entr = Entry(dialog)
    xy_angle_entr.place_configure(x=10, y=76, width=45)
    xy_angle_entr.insert('end', str(xy_angle))

    yz_angle_entr = Entry(dialog)
    yz_angle_entr.place_configure(x=75, y=76, width=45)
    yz_angle_entr.insert('end', str(yz_angle))
    yz_angle_entr.configure(state='disabled')

    itp_entr.bind('<Return>', iupdate)
    x_entr.bind('<Return>', iupdate)
    y_entr.bind('<Return>', iupdate)
    z_entr.bind('<Return>', iupdate)
    width_entr.bind('<Return>', iupdate)
    height_entr.bind('<Return>', iupdate)
    depth_entr.bind('<Return>', iupdate)
    xy_angle_entr.bind('<Return>', iupdate)
    yz_angle_entr.bind('<Return>', iupdate)

    def commit(*args):
        dialog.destroy()

    def cancel(*args):
        OBJECTS.pop(-1)
        update()
        dialog.destroy()

    but_commit = Button(dialog, text='ok', background='green', command=commit)
    but_commit.place_configure(x=80, y=107, width=20)

    but_cancel = Button(dialog, text='cancel', background='red', command=cancel)
    but_cancel.place_configure(x=120, y=107, width=60)

    dialog.mainloop()


master.bind('<ButtonPress 1>', create_object)


def update():
    global DRONEX, DRONEY
    canvas.delete('map')

    if 2.1 >= scale.get() >= 1:
        DRONEX -= DXM
        DRONEY -= DYM
        for i in range(300, -Masshtabe, -Masshtabe):
            if (i + DRONEY * Masshtabe - 300) // Masshtabe % 10 == 0:
                canvas.create_line(0, i - DRONEY * Masshtabe % Masshtabe,
                                   600, i - DRONEY * Masshtabe % Masshtabe, tags=['map'], width=2, stipple='gray50')
            else:
                st = 'gray50'
                canvas.create_line(0, i - DRONEY * Masshtabe % Masshtabe,
                                   600, i - DRONEY * Masshtabe % Masshtabe, tags=['map'], stipple=st)
            if (i + DRONEX * Masshtabe - 300) // Masshtabe % 10 == 0:
                canvas.create_line(i - DRONEX * Masshtabe % Masshtabe, 0,
                                   i - DRONEX * Masshtabe % Masshtabe, 600, tags=['map'], width=2, stipple='gray50')
            else:
                st = 'gray50'
                canvas.create_line(i - DRONEX * Masshtabe % Masshtabe, 0,
                                   i - DRONEX * Masshtabe % Masshtabe, 600, tags=['map'], stipple=st)
        for i in range(300, 600 + Masshtabe, Masshtabe):
            if (i + DRONEY * Masshtabe - 300) // Masshtabe % 10 == 0:
                canvas.create_line(0, i - DRONEY * Masshtabe % Masshtabe,
                                   600, i - DRONEY * Masshtabe % Masshtabe, tags=['map'], width=2, stipple='gray50')
            else:
                st = 'gray50'
                canvas.create_line(0, i - DRONEY * Masshtabe % Masshtabe,
                                   600, i - DRONEY * Masshtabe % Masshtabe, tags=['map'], stipple=st)
            if (i + DRONEX * Masshtabe - 300) // Masshtabe % 10 == 0:
                canvas.create_line(i - DRONEX * Masshtabe % Masshtabe, 0,
                                   i - DRONEX * Masshtabe % Masshtabe, 600, tags=['map'], width=2, stipple='gray50')
            else:
                st = 'gray50'
                canvas.create_line(i - DRONEX * Masshtabe % Masshtabe, 0,
                                   i - DRONEX * Masshtabe % Masshtabe, 600, tags=['map'], stipple=st)
        DRONEX += DXM
        DRONEY += DYM
    elif scale.get() <= 1:
        DRONEX -= DXM
        DRONEY -= DYM
        for i in range(300, -10 * Masshtabe, -10 * Masshtabe):
            canvas.create_line(0, i - DRONEY * Masshtabe % (10 * Masshtabe),
                               600, i - DRONEY * Masshtabe % (10 * Masshtabe), tags=['map'], width=2, stipple='gray50')
            canvas.create_line(i - DRONEX * Masshtabe % (10 * Masshtabe), 0,
                               i - DRONEX * Masshtabe % (10 * Masshtabe), 600, tags=['map'], width=2, stipple='gray50')

        for i in range(300, 600 + 10 * Masshtabe, 10 * Masshtabe):
            canvas.create_line(0, i - DRONEY * Masshtabe % (10 * Masshtabe),
                               600, i - DRONEY * Masshtabe % (10 * Masshtabe), tags=['map'], width=2, stipple='gray50')
            canvas.create_line(i - DRONEX * Masshtabe % (10 * Masshtabe), 0,
                               i - DRONEX * Masshtabe % (10 * Masshtabe), 600, tags=['map'], width=2, stipple='gray50')
        DRONEX += DXM
        DRONEY += DYM
    else:
        DRONEX -= DXM
        DRONEY -= DYM
        step = round(-0.1 * Masshtabe)
        for i in range(300, step, step):
            if (i + DRONEY * Masshtabe - 300) // -step % 100 == 0:
                canvas.create_line(0, i - DRONEY * Masshtabe % -step,
                                   600, i - DRONEY * Masshtabe % -step, tags=['map'], width=4, stipple='gray50')
            elif (i + DRONEY * Masshtabe - 300) // -step % 10 == 0:
                canvas.create_line(0, i - DRONEY * Masshtabe % -step,
                                   600, i - DRONEY * Masshtabe % -step, tags=['map'], width=2, stipple='gray50')
            else:
                st = 'gray50'
                canvas.create_line(0, i - DRONEY * Masshtabe % -step,
                                   600, i - DRONEY * Masshtabe % -step, tags=['map'], stipple=st)
            if (i + DRONEX * Masshtabe - 300) // -step % 100 == 0:
                canvas.create_line(i - DRONEX * Masshtabe % -step, 0,
                                   i - DRONEX * Masshtabe % -step, 600, tags=['map'], width=4, stipple='gray50')
            elif (i + DRONEX * Masshtabe - 300) // -step % 10 == 0:
                canvas.create_line(i - DRONEX * Masshtabe % -step, 0,
                                   i - DRONEX * Masshtabe % -step, 600, tags=['map'], width=2, stipple='gray50')
            else:
                st = 'gray50'
                canvas.create_line(i - DRONEX * Masshtabe % -step, 0,
                                   i - DRONEX * Masshtabe % -step, 600, tags=['map'], stipple=st)
        for i in range(300, 600 - step, -step):
            if (i + DRONEY * Masshtabe - 300) // -step % 100 == 0:
                canvas.create_line(0, i - DRONEY * Masshtabe % -step,
                                   600, i - DRONEY * Masshtabe % -step, tags=['map'], width=4, stipple='gray50')
            elif (i + DRONEY * Masshtabe - 300) // -step % 10 == 0:
                canvas.create_line(0, i - DRONEY * Masshtabe % -step,
                                   600, i - DRONEY * Masshtabe % -step, tags=['map'], width=2, stipple='gray50')
            else:
                st = 'gray50'
                canvas.create_line(0, i - DRONEY * Masshtabe % -step,
                                   600, i - DRONEY * Masshtabe % -step, tags=['map'], stipple=st)
            if (i + DRONEX * Masshtabe - 300) // -step % 100 == 0:
                canvas.create_line(i - DRONEX * Masshtabe % -step, 0,
                                   i - DRONEX * Masshtabe % -step, 600, tags=['map'], width=4, stipple='gray50')
            elif (i + DRONEX * Masshtabe - 300) // -step % 10 == 0:
                canvas.create_line(i - DRONEX * Masshtabe % -step, 0,
                                   i - DRONEX * Masshtabe % -step, 600, tags=['map'], width=2, stipple='gray50')
            else:
                st = 'gray50'
                canvas.create_line(i - DRONEX * Masshtabe % -step, 0,
                                   i - DRONEX * Masshtabe % -step, 600, tags=['map'], stipple=st)
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

            canvas.create_polygon(*points, fill='grey', tags=['map', 'move', 'obj'])

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

            canvas.create_polygon(*p1, *p2, *p3, *p4, fill='grey',
                                  tags=['map', 'move', 'obj'])

    canvas.move('obj', DXM * Masshtabe, DYM * Masshtabe)
    canvas.move('move', 300, 300)

    master.update()


def aim(event):
    canvas.delete('motion')
    x, y = event.x, event.y
    x -= 300
    y -= 300
    if 1 <= scale.get() <= 2.1:
        x, y = x - DXM * Masshtabe % Masshtabe, y - DYM * Masshtabe % Masshtabe
        x, y = round(x / Masshtabe), round(y / Masshtabe)
        x, y = x - DXM + DXM * Masshtabe % Masshtabe / Masshtabe, y - DYM + DYM * Masshtabe % Masshtabe / Masshtabe
        xa, \
        ya = \
            (x + DXM) * Masshtabe + 300, \
            (y + DYM) * Masshtabe + 300
        canvas.create_oval(xa-3, ya-3, xa+3, ya+3, fill='gold', tags=['motion'])
    elif scale.get() <= 1:
        x, y = x - DXM * Masshtabe % (10 * Masshtabe), y - DYM * Masshtabe % (10 * Masshtabe)
        x, y = round(x / Masshtabe / 10), round(y / Masshtabe / 10)
        x, y = x * 10 - DXM + DXM * Masshtabe % (10 * Masshtabe) / Masshtabe, \
               y * 10 - DYM + DYM * Masshtabe % (10 * Masshtabe) / Masshtabe
        xa, \
        ya = \
            (x + DXM) * Masshtabe + 300, \
            (y + DYM) * Masshtabe + 300
        canvas.create_oval(xa - 3, ya - 3, xa + 3, ya + 3, fill='gold', tags=['motion'])
    else:
        x, y = x - DXM * Masshtabe % (0.1 * Masshtabe), y - DYM * Masshtabe % (0.1 * Masshtabe)
        x, y = round(x / Masshtabe / 0.1), round(y / Masshtabe / 0.1)
        x, y = x * 0.1 - DXM + DXM * Masshtabe % (0.1 * Masshtabe) / Masshtabe, \
               y * 0.1 - DYM + DYM * Masshtabe % (0.1 * Masshtabe) / Masshtabe
        xa, \
        ya = \
            (x + DXM) * Masshtabe + 300, \
            (y + DYM) * Masshtabe + 300
        canvas.create_oval(xa - 3, ya - 3, xa + 3, ya + 3, fill='gold', tags=['motion'])
    update()

# master.bind('<ButtonPress 3>', restMapD)


master.bind('<Motion>', aim)


def scale2(event):
    ins = scale.get()
    ins += event.delta / 120 * 0.05
    ins = max(0.5, min(ins, 3))
    scale.set(ins)
    update()


master.bind('<MouseWheel>', scale2)

while True:
    update()
