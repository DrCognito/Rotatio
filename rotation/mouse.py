'''Adapted from mse_fun.py from:
[Mouse Sensitivity Exporter](http://mousesensexport.sourceforge.net/)
Credit to GrosBedo and Skip Montanaro.
'''
from ctypes import *
from ctypes.wintypes import DWORD
import time
from collections import namedtuple

#C structs from mse

PUL = POINTER(c_ulong)

mouse_dwFlags = namedtuple("mouse_dwFlags", ["MOUSEEVENTF_ABSOLUTE",
                                             "MOUSEEVENTF_HWHEEL",
                                             "MOUSEEVENTF_MOVE",
                                             "MOUSEEVENTF_MOVE_NOCOALESCE",
                                             "MOUSEEVENTF_LEFTDOWN",
                                             "MOUSEEVENTF_LEFTUP",
                                             "MOUSEEVENTF_RIGHTDOWN",
                                             "MOUSEEVENTF_RIGHTUP",
                                             "MOUSEEVENTF_MIDDLEDOWN",
                                             "MOUSEEVENTF_MIDDLEUP",
                                             "MOUSEEVENTF_VIRTUALDESK",
                                             "MOUSEEVENTF_WHEEL",
                                             "MOUSEEVENTF_XDOWN",
                                             "MOUSEEVENTF_XUP"])

mouse_dwFlags.MOUSEEVENTF_ABSOLUTE = 0x8000
mouse_dwFlags.MOUSEEVENTF_HWHEEL = 0x01000
mouse_dwFlags.MOUSEEVENTF_MOVE = 0x0001
mouse_dwFlags.MOUSEEVENTF_MOVE_NOCOALESCE = 0x2000
mouse_dwFlags.MOUSEEVENTF_LEFTDOWN = 0x0002
mouse_dwFlags.MOUSEEVENTF_LEFTUP = 0x0004
mouse_dwFlags.MOUSEEVENTF_RIGHTDOWN = 0x0008
mouse_dwFlags.MOUSEEVENTF_RIGHTUP = 0x0010
mouse_dwFlags.MOUSEEVENTF_MIDDLEDOWN = 0x0020
mouse_dwFlags.MOUSEEVENTF_MIDDLEUP = 0x0040
mouse_dwFlags.MOUSEEVENTF_VIRTUALDESK = 0x4000
mouse_dwFlags.MOUSEEVENTF_WHEEL = 0x0800
mouse_dwFlags.MOUSEEVENTF_XDOWN = 0x0080
mouse_dwFlags.MOUSEEVENTF_XUP = 0x0100


class KeyBdInput(Structure):
    _fields_ = [("wVk", c_ushort),
    ("wScan", c_ushort),
    ("dwFlags", c_ulong),
    ("time", c_ulong),
    ("dwExtraInfo", PUL)]


class HardwareInput(Structure):
    _fields_ = [("uMsg", c_ulong),
    ("wParamL", c_short),
    ("wParamH", c_ushort)]


class MouseInput(Structure):
    _fields_ = [("dx", c_long),
    ("dy", c_long),
    ("mouseData", c_ulong),
    ("dwFlags", DWORD),
    ("time",c_ulong),
    ("dwExtraInfo", PUL)]


class Input_I(Union):
    _fields_ = [("ki", KeyBdInput),
    ("mi", MouseInput),
    ("hi", HardwareInput)]


class Input(Structure):
    _fields_ = [("type", c_ulong),
    ("ii", Input_I)]


class POINT(Structure):
    _fields_ = [("x", c_ulong),
    ("y", c_ulong)]

def mousemove(movex, movey, t=0, delay=10):
    '''Move the mouse pointer by x or y pixels in a time'''
    # This is used to move cursor ouside games and such that won't recognize the SendInput command
    # windll.user32.SetCursorPos(int(x), int(y))
    time.sleep(delay)
    # From set_cursor_pos()
    mousehook = 1
    mousehooktype = 1
    # If the environment tested hook the mouse,
    # then it means we have to only input the number of pixel we want to move,
    # origin is (0,0)
    if (mousehook == 1 and mousehooktype == 1):
        x = movex
        y = movey
    # A variant of mouse hook. This time, the origin is (currentmousex,
    # currentmousey) and since the environment is hooking the mouse, each time
    # we move the mouse the env move back the cursor to origin, so that's why
    # we move the cursor to (currentmousex + numberofpixeltomovex,
    # currentmousey + numberofpixeltomovey)
    elif (mousehook == 1 and mousehooktype == 2):
        currentmousex, currentmousey = queryMousePos()
        x = currentmousex + int(movex)
        y = currentmousey + int(movey)
    # If there isn't any hooking, then we move the current cursor position
    # from numberofpixel, which we iterate (we could capture each time the
    # current cursor position but it would take more calculation and wouldn't
    # work in some cases I tested)
    else:
        currentmousex, currentmousey = queryMousePos()
        x = currentmousex + int(movex)
        y = currentmousey + int(movey)

    extra = c_ulong(0)
    mflag = mouse_dwFlags.MOUSEEVENTF_MOVE
    ii_ = Input_I()
    ii_.mi = MouseInput(int(x), int(y), 0, mflag, t, pointer(extra)) 
    #Here we save the Mouse false input into ii_ object. 
    #MouseInput( x, y, mousedata ?, dwFlag (2 to click, 4 to release), time, extra infos)
    #https://msdn.microsoft.com/en-us/library/windows/desktop/ms646273(v=vs.85).aspx

    arrx = Input(0, ii_)
    print(arrx)

    #SendInput( number of actions or items in array, pointer(array), size of array)
    #https://msdn.microsoft.com/en-us/library/windows/desktop/ms646310(v=vs.85).aspx
    inputOut = windll.user32.SendInput(1, pointer(arrx), sizeof(arrx))
    print(inputOut)

    orig = POINT()
    windll.user32.GetCursorPos(byref(orig))

    return orig.x, orig.y

def queryMousePos():
    '''https://stackoverflow.com/questions/3698635/getting-cursor-position-in-python'''
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x, pt.y
