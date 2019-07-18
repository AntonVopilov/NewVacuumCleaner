import math as mp
import random
from random import randint, choice
import new_body_maker as bm


def hurdle_fabric(max_x, max_y, max_size, num_hurdles, x, y, size):
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
        x_tr = randint(2, max_x - 2)
        y_tr = randint(2, max_y - 2)
        angle = choice(angles)

        for point in hurdle.get_all_body_points(x_tr, y_tr, angle):
            if (x - size < point[0] < x + size) and (y - size < point[1] < y + size):
                continue
            elif (0 < point[0] < max_x) and (0 < point[1] < max_y):
                hurdles.add(point)
    for x in range(max_x):
        hurdles.add((x, 0))
        hurdles.add((x, max_y - 1))
    for y in range(max_y):
        hurdles.add((0, y))
        hurdles.add((max_x - 1, y))
    return hurdles



def create_map_window(window, hurdles, char):
    for point in hurdles:
        try:
            window.addch(point[1], point[0], char)
        except:
            with open('error_points.txt', 'w') as file:
                file.write(str(point))
    return hurdles


if __name__ == '__main__':
    max_x = 40
    max_y = 20
    num = 10
    max_size = 4

    hurdles = create_map_window(None, '#', max_x, max_y, max_size, num)
    print(hurdles)
