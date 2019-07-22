import curses
import math as mp
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_F1, KEY_F2
from functools import lru_cache

import body_maker as mb

commands = {KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_F1, KEY_F2}
ROB_SIZE = 5


class Robot(object):

    def __init__(self, x_pos, y_pos, angle, r, map_obj):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.angle = angle
        self.angle_step = - mp.pi / 10

        # self.body = mb.CircleBody(r)
        self.body = mb.RectangleBody(r, r)
        self.size = r

        self.map_obj = map_obj
        self.collision = False

        self.order_pnts, self.special_pnts = self.get_current_robot_points()
        self.prev_body = self.get_all_robot_points(x_pos, y_pos, angle)

        self.body.order_char = '@'
        self.body.special_char = '*'

        self.move_dict = {
            KEY_UP: self.up,
            KEY_DOWN: self.down,
            KEY_LEFT: self.left,
            KEY_RIGHT: self.right,
            KEY_F1: self.rotate_left,
            KEY_F2: self.rotate_right
        }

    def up(self, x, y, angle):
        return x, y - 1, angle

    def down(self, x, y, angle):
        return x, y + 1, angle

    def left(self, x, y, angle):
        return x - 1, y, angle

    def right(self, x, y, angle):
        return x + 1, y, angle

    def rotate_left(self, x, y, angle):
        return x, y, angle + self.angle_step

    def rotate_right(self, x, y, angle):
        return x, y, angle - self.angle_step

    @lru_cache(3)
    def get_robot_points(self, x, y, angle):
        return self.body.render_body(x, y, angle)

    def get_all_robot_points(self, x, y, angle):
        return self.body.get_all_body_points(x, y, angle)

    def get_current_robot_points(self):
        return self.get_robot_points(self.x_pos, self.y_pos, self.angle)

    def make_move(self, command):
        x, y, angle = self.x_pos, self.y_pos, self.angle
        if command:
            x, y, angle = self.move_dict[command](x, y, angle)

        order, special = self.get_robot_points(x, y, angle)
        new_points = order.union(special)

        if any(point in self.map_obj for point in new_points):
            self.collision = True
        else:
            self.prev_body = self.get_all_robot_points(self.x_pos, self.y_pos,
                                                       self.angle)
            self.x_pos, self.y_pos, self.angle = x, y, angle
            self.order_pnts = order
            self.special_pnts = special
            self.collision = False

    def update_scr(self, window, color_pair, command):
        self.make_move(command)
        if not self.collision:
            color = color_pair[0]
            for point in self.prev_body:
                window.addstr(point[1], point[0], ' ')
        else:
            color = color_pair[1]
        for point in self.order_pnts:
            window.addstr(point[1], point[0], self.body.order_char)
        for point in self.special_pnts:
            window.addstr(point[1], point[0], self.body.special_char, color)

    def get_view_box(self, scr_wd, scr_len, map_wd, map_len):
        x, y = self.get_position()

        if map_wd < scr_wd:
            x = 0
        else:
            x = max(0, x - 3 * self.size)

        if map_len < scr_len:
            y = 0
        else:
            y = max(0, y - self.size)
        return y, x, 2, 1, scr_len - 1, scr_wd - 1

    def get_position(self):
        return self.x_pos, self.y_pos

    def get_collision(self):
        return self.collision

