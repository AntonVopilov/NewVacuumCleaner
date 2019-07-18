from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_F1, KEY_F2
import math as mp
import new_body_maker as mb

commands = {KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_F1, KEY_F2}

class Robot(object):

    def __init__(self, x_pos, y_pos, angle, r, map_obj):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.angle = angle
        self.angle_step = - mp.pi / 10

        # self.body = mb.CircleBody(r)
        self.body = mb.ReqtangleBody(r, r)
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

    # @cashe

    def get_robot_points(self, x, y, angle):
        return self.body.render_body(x, y, angle)

    def get_all_robot_points(self, x, y, angle):
        return self.body.get_all_body_points(x, y, angle)

    def get_current_robot_points(self):
        return self.get_robot_points(self.x_pos, self.y_pos, self.angle)



    def make_move(self, command):
        x, y, angle = self.x_pos, self.y_pos, self.angle
        x, y, angle = self.move_dict[command](x, y, angle)

        order, special = self.get_robot_points(x, y, angle)
        new_points = order.union(special)

        if any(point in self.map_obj for point in new_points):
            self.collision = True
        else:
            self.prev_body = self.get_all_robot_points(self.x_pos, self.y_pos, self.angle)
            self.x_pos, self.y_pos, self.angle = x, y, angle
            self.order_pnts = order
            self.special_pnts = special
            self.collision = False

    def update_scr(self, window, command):
        self.make_move(command)
        if not self.collision:
            for point in self.prev_body:
                window.addch(point[1], point[0], ' ')
            for point in self.order_pnts:
                window.addch(point[1], point[0], self.body.order_char)
            for point in self.special_pnts:
                window.addch(point[1], point[0], self.body.special_char)

    def get_view_box(self, scr_wd, scr_len):
        x = max(0, self.x_pos - 2 * self.size)
        y = max(0, self.y_pos - 2 * self.size)
        return y, x, 1, 1, scr_len - 1, scr_wd // 2

import curses
def main(stdscr):

    robot = Robot(6, 6, 0, 5, [])
    robot.update_scr(stdscr, KEY_UP)
    stdscr.refresh()

    while True:
        event = stdscr.getch()
        if event not in commands:
            break
        robot.update_scr(stdscr, event)
        stdscr.refresh()
if __name__ == '__main__':
    curses.wrapper(main)


