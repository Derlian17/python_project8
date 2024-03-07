from tkinter import *



master = Tk()
canvas = Canvas(master, width=600, height=600)
canvas.pack()

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

master.mainloop()