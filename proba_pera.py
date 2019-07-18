import curses
import new_map as nm
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_F1, KEY_F2
import new_robot as rob
import time

def main(stdscr):
    stdscr.clear()
    stdscr.keypad(1)
    curses.noecho()
    curses.curs_set(0)

    scr_length, scr_width = stdscr.getmaxyx()

    stdscr.clear()
    stdscr.refresh()

    max_x = 40
    max_y = 20
    num = 10
    max_size = 4

    pad = curses.newpad(max_x+4, max_y+4)
    view_box = [1, 1, scr_length - 1, scr_width // 2]


    hurdles = nm.create_map_window(pad, '#', max_x, max_y, max_size, num)
    pad.refresh(0, 0, view_box[0], view_box[1], view_box[2], view_box[3])


    # robot_object = rob.Robot(max_x//2, max_y//2, 0, 4, hurdles)
    # robot_object.update_scr(stdscr, KEY_UP)

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
    curses.wrapper(main)