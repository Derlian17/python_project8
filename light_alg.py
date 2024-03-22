from math import atan, sin, cos, acos
from math import pi

DRONH = 0.84  # размеры дрона. не используются
DRONW = 1  # размеры дрона. не используются
DRONL = 3  # размеры дрона. не используются

start_coord = [0, 0, 0]  # корординаты: начальная, конечная и дрона
dron_coord = [0, 0, 0]  # корординаты: начальная, конечная и дрона
end_coord = [0, 70, 0]  # корординаты: начальная, конечная и дрона
dron_degr = 0  # угол поворота дрона
past_dist = 0  # расстояние с датчика предыдущее и нынешнее
dist = 0  # расстояние с датчика предыдущее и нынешнее

'''Краткое введение. данный алгоритм - работает. это уже хорошо.  ̶П̶л̶о̶х̶о̶ ̶т̶о̶ ̶ч̶т̶о̶ ̶о̶н̶ ̶н̶е̶ ̶у̶ч̶и̶т̶ы̶в̶а̶е̶т̶ ̶с̶в̶о̶и̶ ̶г̶а̶б̶а̶р̶и̶т̶ы̶. 
Также в этом файле присутствует экспериментальная часть - дрон стремится всегда быть на расстоянии 0.7 метров от стены, 
когда ее видит (я пометил #!). алгоритм движения реализован через правило правой руки, т.е. оптимальности от него ждать 
не надо и вполне возможно что можно загнать в вечный цикл. ̶ ̶е̶с̶л̶и̶ ̶х̶о̶т̶и̶т̶е̶ ̶т̶е̶с̶т̶и̶р̶о̶в̶а̶т̶ь̶ ̶п̶о̶с̶т̶а̶в̶ь̶т̶е̶ ̶в̶ ̶ф̶а̶й̶л̶е̶ ̶ ̶s̶i̶m̶_̶s̶h̶o̶w̶.̶p̶y̶
̶S̶U̶B̶P̶O̶I̶N̶T̶S̶ ̶=̶ ̶[̶(̶0̶,̶ ̶0̶,̶ ̶0̶)̶]̶ ̶ ̶и̶л̶и̶ ̶д̶р̶о̶н̶ ̶р̶а̶з̶о̶б̶ь̶е̶т̶с̶я̶. функции Step, Round, Find_dist были взяты из прошлого алгоритма и 
изменены не были. работают ибо ломаться там уже нечему. функции length и Shortest_route были написаны полностью мною и 
многократно проверены. Лезть НЕ надо. Функции It_is_finish и Adjust были мною же частично переписаны. за It_is_finish 
также ручаюсь. Adjust работает, но из-за погрешности датчика дает разброс до 10 градусов. также есть вероятность что в 
очень узких коридорах дрон из-за неее врежется (см #!). не учитывает ширину прохода. in_line. написана мною от и до. 
Из-за ее простоты багов там быть не должно, но если случатся первым делом смотрите sh <= 0. Look_forward - опять же моя. 
не тестирована ни разу.'''


def Step(x):  # движение вперед
    dron_coord[0] += x * sin(dron_degr / 180 * pi)  # изменить собственные координаты
    dron_coord[1] += x * cos(dron_degr / 180 * pi)  # изменить собственные координаты
    with open("log.txt", "a") as file:  # записать в файл команду на движение вперед
        file.write(f"B move({x})\n")  # записать в файл команду на движение вперед
    Find_dist()  # ожидание ответа


def Round(x):  # поворот
    global dron_degr  # изменить собственную перемену градуса
    dron_degr += round(x, 2)  # изменить собственную перемену градуса
    with open("log.txt", "a") as file:  # записать в файл команду на поворот
        file.write(f"B rotate({round(x, 2)})\n")  # записать в файл команду на поворот
    Find_dist()  # ожидание ответа


def Find_dist():  # ожидание ответа
    global past_dist  # запись предыдущего значения
    global dist  # запись предыдущего значения
    past_dist = dist  # запись предыдущего значения
    f = True  # флаг - переменная на прекращение цикла
    while f:
        with open('log.txt') as file:  # открытие файла
            end = file.readlines()[-1]   # считывание последней строки
            if end[0] == 'S':  # проверка что это ответ
                dist = round(float(end[1:]), 2)  # запись расстояния. округляется т.к. разрешение датчика 1 см
                f = False  # опускаем флаг - вырубаем цикл


def It_is_finish():  # проверка на финиш
    if length(dron_coord, end_coord) <= 2:  # проверка на расстояние между дроном и концом
        return 1
    else:
        return 0


def Adjust(st_degr=10):  # встать параллельно препятствию . не ставить параметр меньше 10
    if st_degr == 0:  # если параметр 0
        Adjust(-10)  # если параметр 0
        return  # если параметр 0
    Round(st_degr)  # поворот - посмотреть что справа
    otr = round((dist ** 2 + past_dist ** 2 - 2 * dist * past_dist * cos(st_degr / 180 * pi)) ** 0.5, 2)  # вычисление
    #                                                                                       расстояния между точками,
    #                                                                                       замеченными сканером
    degr = 180 - acos((otr ** 2 + past_dist ** 2 - dist ** 2) / (2 * otr * past_dist)) / pi * 180  # вычисление угла на
    #                                                                                    который нужно повернуться чтобы
    #                                                                                    стать параллельным
    degr = round(degr, 2)
    step = 1  # на сколько м движимся
    if dist == -1:  # если справа ничего - встаем в прежнюю позицию и движимся
        Round(-st_degr)  # встать в прежнюю позицию
        Adjust(st_degr-10)
    else:
        Round(-st_degr)  # поворачиваемся на стартовую позицию
        Round(degr)  # поворачиваемся параллельно
        if Look_forward(step):  # если проход достаточно широк
            Step(step)  # движимся параллельно
            Round(-90)  # #!! встаем условно-перпендикулярно (угол вычисляется неточно из-за погрешности датчика)
            if 0 < dist:  # #!        если есть препятствие
                Step(dist - 0.7)  # #!  встаем к стене на расстояние 0.7 м
        else:
            Round(-degr+90)  # повернулись параллельно прежнему пряпятствию
            Step(step)  # опять же вперед
            Round(-90)
        print(degr)


def Shortest_route():  # угол до конечной точки. работает. не трогайте 🙏🙏
    chetvert = ''
    x0, y0 = end_coord[:2]  # ввод координат под другим именем - программа скопирована из другого проекта
    cx, cy = dron_coord[:2]  # ввод координат под другим именем - программа скопирована из другого проекта
    if x0 > cx and y0 >= cy:  # вычисление текущей четверти
        chetvert = 'I'  # вычисление текущей четверти
    elif x0 > cx and y0 < cy:  # вычисление текущей четверти
        chetvert = 'IV'  # вычисление текущей четверти
    elif y0 >= cy:  # вычисление текущей четверти
        chetvert = 'II'  # вычисление текущей четверти
    else:  # вычисление текущей четверти
        chetvert = 'III'  # вычисление текущей четверти
    try:
        angle_f = -atan((y0 - cy) / (x0 - cx)) + pi / 2  # вычисление угла
        if chetvert in ['I', 'IV']:  # компенсирование особенностей тангенса
            pass  # компенсирование особенностей тангенса
        else:  # компенсирование особенностей тангенса
            angle_f = angle_f + pi  # компенсирование особенностей тангенса
    except ZeroDivisionError:  # если иксы совпадают
        if chetvert == 'II':  # если иксы совпадают
            angle_f = 0  # если иксы совпадают
        else:  # если иксы совпадают
            angle_f = pi  # если иксы совпадают

    angle_f = angle_f / pi * 180
    if angle_f > 180:
        angle_f = angle_f - 360
    return angle_f  # возврат угла в градусах


def Look_forward(rasst=1):  # смотрим влезем ли если правый бок параллелен
    ang = atan(DRONW / DRONH)  # угол дрона
    Round(ang / pi * 180)  # посмотреть на крайнюю левую точку
    raast2 = dist  # сохранить расстояние до препятствия
    Round(-ang / pi * 180)  # вернуться на прежний угол
    if raast2 == -1:  # если пусто то точно влезем
        return True  # если пусто то точно влезем
    return raast2 * cos(ang) >= rasst + 0.2  # если расстояние больше того на которое мы двигаемся - то влезем


def length(p1, p2):  # вычисление длины между точками. работает!!
    s = 0  # введение переменной
    for i in range(len(p1)):  # перебор индексов
        s += (p1[i] - p2[i]) ** 2  # добавление квадратов разностей
    return s ** 0.5  # вывод корня суммы


def in_line():  # вычисление расстояния от дрона до линии старт-конец
    l1 = length(dron_coord, start_coord)  # вычисление расстояния дрон-старт
    l2 = length(dron_coord, end_coord)  # вычисление расстояния дрон-конец
    l3 = length(start_coord, end_coord)  # вычисление расстояния страт-конец

    p = (l1 + l2 + l3) / 2  # полупериметр
    sh = (p * (p - l1) * (p - l2) * (p - l3))  # квадрат площади Герона
    if sh <= 0:  # если площадь меньше нуля - понять не могу как это возможно - но есть
        return True  # принадлежит
    sh **= 0.5  # иначе извлекаем корень из площади

    h_real = sh * 2 / l3  # и вычисляем высоту

    return h_real < 2  # возвращаем истину если расстояние меньше 2 м


if __name__ == '__main__':  # если запущен этот файл
    Round(Shortest_route() - dron_degr)  # поворачиваемся к цели
    Run = True  # переменная на прерывание цикла
    while Run:  # сам цикл
        if (dist >= 3 or dist == -1) and not in_line():  # если впереди пусто и мы не на на линии старт-конец
            Round(Shortest_route() - dron_degr)  # поворачиваемся
        if dist >= 3 or dist == -1:  # если впереди пусто
            if It_is_finish():  # если мы в конце времен и карты
                Run = False  # опускаем флаг
                with open('log.txt', 'a') as file:  # записываем что победили
                    print('B Finish()', file=file)  # записываем что победили
                break  # прерываем цикл (флаг здесь не нужен... удаляйте сами, мне лень)

            Step(1)  # движимся вперед не более 2
        else:  # иначе
            Adjust()  # используем правило правой руки
