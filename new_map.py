import math as mp
import random
from random import randint, choice
import new_body_maker as bm


def hurdle_fabric(max_x, max_y, max_size, num_hurdles):
    """
    Функция генерирует препятсвия случайного размера и в случайном положении
    max_x - крайннее допустимое значение по оси х
    max_y - крайннее допустимое значение по оси y
    max_size - максимальный размер препятсивия
    num_hurdles - количество препятсвий
    """
    if any(not isinstance(arg, int) for arg in
           [max_x, max_y, max_size, num_hurdles]):
        raise TypeError(f'Expected int arguments')

    angles = [mp.pi / 10 * i for i in range(11)]

    hurdles = set()
    for i in range(num_hurdles):
        hurdle = choice(
            [bm.ReqtangleBody(randint(1, max_size), randint(1, max_size)),
             bm.CircleBody(randint(1, max_size))])
        size = hurdle.get_max_size()


        x_tr = randint(size + 1, max_x  - size - 1)
        y_tr = randint(size + 1, max_y - size - 1)
        angle = choice(angles)

        for point in hurdle.get_all_body_points(x_tr, y_tr, angle):
            hurdles.add(point)
    return hurdles

def create_map_window(window, char, max_x, max_y, max_size, num_hurdles):
    hurdles = hurdle_fabric(max_x, max_y, max_size, num_hurdles)
    for point in hurdles:
        window.addch(point[1], point[0], char)
    return hurdles

