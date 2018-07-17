#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import tty, termios
import sys
if sys.version_info.major < 3:
    import thread as _thread
else:
    import _thread
import time


try:
    from msvcrt import getch  # try to import Windows version
except ImportError:
    def getch():   # define non-Windows version
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

char = None
def start_keylogger():
    _thread.start_new_thread(keypress, ())

def stop_keylogger():
    _thread.exit()

def keypress():
    global char
    char = getch()

def GetAsyncKeyState(charPressed):
    global char
    if char is not None:
        print("CHAR : " + char)
        try:
            print("Key pressed is " + char)
        except UnicodeDecodeError:
            print("character can not be decoded, sorry!")
            char = None
        if char == charPressed:
            return charPressed.index(char)
    else:
        return 5
"""
if __name__ == "__main__":
    print(GetAsyncKeyState(["w", "a", "s", "d", " "]))
"""
