#!/usr/bin/env python3

# v.0.6
# 14.06.18, 00:31

from game import Game
import curses

if __name__ == "__main__":
    try:
        x = Game()
        x.start()
    finally:
        curses.endwin()
