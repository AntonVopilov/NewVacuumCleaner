import math as mp
import functools
from functools import lru_cache
angles = [mp.pi / 10 * i for i in range(11)]

@lru_cache(len(angles))
def rotation_matrix(angle):
    """Calculated rotation matrix"""
    res_matrix = [[0, 0], [0, 0]]
    res_matrix[0][0] = mp.cos(angle)
    res_matrix[0][1] = - mp.sin(angle)
    res_matrix[1][1] = res_matrix[0][0]
    res_matrix[1][0] = - res_matrix[0][1]
    return res_matrix


def rotation(vec, angle):
    """Rotate vector"""
    mtrx = rotation_matrix(angle)
    return round(vec[0] * mtrx[0][0] + vec[1] * mtrx[0][1]), \
           round(vec[0] * mtrx[1][0] + vec[1] * mtrx[1][1])


def transition(vec, x, y):
    """Translate vector"""
    return vec[0] + x, vec[1] + y


def replace_vec(vec, x, y, angle):
    """Rotate and translate vector"""
    res_vec = rotation(vec, angle)
    return transition(res_vec, x, y)


class AbstractBody:
    """AbstractBody return body with methods:
    get_max_size - return max size, should be implement in concrete body-class,
    set_body_points - calculate body points at (x=0, y=0, angle=0),
    get_zero_body_points - return points, which were calculated
    by set_body_points,
    render_body - calculate body points at concrete position;
    There are attributes:

    """
    def __init__(self, *args, **kwargs):
        self.body_points = {
            'order': set(),
            'special': set()
        }
        self.set_body_points()
        self.order_char = ''
        self.special_char = ''

    def get_max_size(self):
        pass

    def set_body_points(self):
        pass

    def get_zero_body_points(self):
        return self.body_points['order'], self.body_points['special']

    def render_body(self, x_pos, y_pos, angle):
        order_zero, special_zero = self.get_zero_body_points()
        order, special = set(), set()
        for point in order_zero:
            order.add(replace_vec(point, x_pos, y_pos, angle))

        for point in special_zero:
            special.add(replace_vec(point, x_pos, y_pos, angle))
        return order, special

    def get_all_body_points(self, x_pos, y_pos, angle):
        order, special = self.render_body(x_pos, y_pos, angle)
        return order.union(special)


class RectangleBody(AbstractBody):

    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.char = ''
        super().__init__()

    def get_max_size(self):
        return max(self.width, self.length)

    def calculate_transition_vec(self):
        x_tr, y_tr = None, None
        if self.width % 2 != 0:
            x_tr = -self.width // 2 + 1
        else:
            x_tr = -self.width // 2

        if self.length % 2 != 0:
            y_tr = -self.length // 2 + 1
        else:
            y_tr = -self.length // 2
        return x_tr, y_tr

    def set_body_points(self):
        buffer_points = set()
        for x in range(self.width):
            for y in range(self.length):
                buffer_points.add((x, y))

        x_tr, y_tr = self.calculate_transition_vec()

        for point in buffer_points:
            self.body_points['order'].add(
                transition(point, x_tr, y_tr))

        for x in range(self.width):
            self.body_points['special'].add(
                transition((x, 0), x_tr, y_tr))


class CircleBody(AbstractBody):
    def __init__(self, r):
        self.radius = r
        self.char = ''
        super().__init__()

    def get_max_size(self):
        return self.radius

    def set_body_points(self):
        buffer_body = set()
        for x in range(1, self.radius):
            y_max = round(mp.sqrt(self.radius ** 2 - (x + 1) ** 2))

            if y_max != 0:
                for y in range(y_max):
                    buffer_body.add((x, y))
                    buffer_body.add((x, - y))
            else:

                buffer_body.add((x, y_max))

        for point in buffer_body:
            self.body_points['order'].add(point)
            self.body_points['order'].add(rotation(point, mp.pi))

        for y in range(round(mp.sqrt(self.radius ** 2))):
            self.body_points['special'].add((0, y))
            self.body_points['special'].add((0, -y))


