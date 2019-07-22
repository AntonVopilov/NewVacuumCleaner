import curses
import argparse

import map_constructor as nm
import robot as rob


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
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    color_pair = [curses.color_pair(1), curses.color_pair(2)]

    scr_length, scr_width = stdscr.getmaxyx()

    msg_list = ['Vacuum Cleaner',
                'Press any key to continue',
                'to EXIT press key accept control keys',
                'control keys: up, down, left, right',
                'F1/F2 - rotation'
                ]
    for i, msg in enumerate(msg_list):
        stdscr.addstr(scr_length // 2 - len(msg_list) // 2 + i,
                      scr_width // 2 - len(msg) // 2, msg)
    stdscr.getch()
    stdscr.clear()
    stdscr.refresh()

    max_size = min(map_length, map_length) * 5 // 100

    map_pad = curses.newpad(map_length + 2, map_width + 2)
    map_obj = nm.MapConstructor(map_width, map_length, max_size,
                                hurdles_count)

    map_list = map_obj.get_coord_list(map_width // 2, map_length // 2,
                                      rob.ROB_SIZE)
    map_obj.update_map_scr(map_pad, '#')

    robot = rob.Robot(map_width // 2, map_length // 2, 0, rob.ROB_SIZE,
                      map_list)

    robot.update_scr(map_pad, color_pair, None)
    args = robot.get_view_box(scr_width, scr_length, map_width, map_length)
    map_pad.refresh(*args)

    while True:
        event = stdscr.getch()
        if event not in rob.commands:
            break
        robot.update_scr(map_pad, color_pair, event)
        x_pos, y_pos = robot.get_position()
        position_msg = f'x_pos = {x_pos}, y_pos = {y_pos} '
        collision_msg = f'collision status: {robot.get_collision()}  '

        stdscr.addstr(0, 0, position_msg, color_pair[1])
        stdscr.addstr(1, 0, collision_msg, color_pair[1])

        args = robot.get_view_box(scr_width, scr_length, map_width, map_length)

        map_pad.refresh(*args)


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()

    curses.wrapper(main, namespace.width,
                   namespace.length, namespace.num_hurdles)
