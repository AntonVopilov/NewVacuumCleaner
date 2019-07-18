import curses
import argparse

import new_map as nm
import new_robot as rob
import time

ROB_SIZE = 5


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-wd', '--width', default=100, type=int)
    parser.add_argument('-lg', '--length', default=100, type=int)
    parser.add_argument('-n', '--num_hurdles', default=100, type=int)
    return parser


def main(stdscr, map_width, map_length, hurdles_count):
    stdscr.clear()
    stdscr.keypad(True)
    curses.noecho()
    curses.curs_set(False)
    stdscr.refresh()

    scr_length, scr_width = stdscr.getmaxyx()

    pad = curses.newpad(map_length + 1, map_width + 1)
    x_pos, y_pos = map_width // 2, map_length // 2
    angle = 0

    # hurdles = nm.hurdle_fabric(map_width, map_length, ROB_SIZE, hurdles_count,
    #                            x_pos, y_pos, ROB_SIZE)
    #
    # nm.create_map_window(pad, hurdles, '#')

    robot_object = rob.Robot(x_pos, y_pos, angle, ROB_SIZE, [])
    view_box = robot_object.get_view_box(scr_width, scr_length)
    pad.refresh(*view_box)
    time.sleep(3)
    robot_object.update_scr(stdscr, rob.KEY_UP)
    time.sleep(10)

    # robot_object = rob.Robot(10, 10, 0, 9, [])
    #
    # while True:
    #     event = stdscr.getch()
    #     if event not in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_F1,
    #                      KEY_F2]:
    #         break
    #
    #     robot_object.update_scr(stdscr, event)


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()

    curses.wrapper(main, namespace.width,
                   namespace.length, namespace.num_hurdles)
