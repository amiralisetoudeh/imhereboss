'''
I'm Here Boss (v1.0)


██╗█╗███╗   ███╗    ██╗  ██╗███████╗██████╗ ███████╗       ██████╗  ██████╗ ███████╗███████╗
██║═╝████╗ ████║    ██║  ██║██╔════╝██╔══██╗██╔════╝       ██╔══██╗██╔═══██╗██╔════╝██╔════╝
██║  ██╔████╔██║    ███████║█████╗  ██████╔╝█████╗         ██████╔╝██║   ██║███████╗███████╗
██║  ██║╚██╔╝██║    ██╔══██║██╔══╝  ██╔══██╗██╔══╝         ██╔══██╗██║   ██║╚════██║╚════██║
██║  ██║ ╚═╝ ██║    ██║  ██║███████╗██║  ██║███████╗▄█╗    ██████╔╝╚██████╔╝███████║███████║
╚═╝  ╚═╝     ╚═╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
                                                                                          

Author: Ali Setoudeh
Copyright (c) 2023

Purpose:
For generating automated movement of the mouse and keyboard strokes with the goal of preventing
a Windows machine from going into idle state (e.g., Windows Screen Saver / Lock Screen,
Microsoft Teams 'Away' Status, and others).


With the default values, this script will do the following:

* Keep track of the current idle time of the system.
* Countdown 4 minutes (240 seconds) to zero.
  * Default timer is set to 4 minutes because Microsoft Teams' idle timer is set to 5 minutes.
* If any mouse movement or keyboard stroke is detected, Idle Time resets to 0 and Countdown resets to 240.
  * This is to prevent the script from moving the mouse and pressing ctrl while you're working.
* Once the countdown reaches zero, the script will slightly move the mouse and hit the ctrl key.
* The countdown timer resets to 240 and the cycle continues.

The net result: Your screen will not lock and your Microsoft Teams + Slack will show you as 'Available'.

Output:
Running the script will generate a PrettyTable with 5 columns:

+-----------------------------------------------------------------------------+
|                               I'm here, Boss!                               |
+-------------+-------------+----------------+-----------------+--------------+
|  Idle Time  |  Countdown  | Mouse Position | Last Ctrl Press | Wiggle Count |
+-------------+-------------+----------------+-----------------+--------------+
| 097 seconds | 143 seconds |   (712, 147)   |     08:35:42    |      23      |
+-------------+-------------+----------------+-----------------+--------------+

* Idle Time: Current idle time on the OS. It resets if mouse movement or keyboard strokes are registered.
* Countdown: Time left before the automatic mouse movement and keyboard strokes are generated.
* Mouse Position: The current position of the mouse cursor on the screen.
* Last Ctrl Press: The time stamp of the ctrl key being pressed.
* Wiggle Count: The number of times the mouse was wiggled by the script


Disclaimner:
This script is meant to be used responsibly (i.e., while at your computer).
Don't have this script running and leave your computer unattended.
Don't run this script if your InfoSec policy prohibits it.
You and only you are responsible for usage of this script.


Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software.

'''

####################################################################################################
# INSTRUCTIONS: Packages
#
# The following packages need to be installed BEFORE running this script:
# >pywin32 (provides win32api and win32con)
# >>>run this command: pip install pywin32
#
# >prettytable (create tables in Python)
# >>>run this command: pip install prettytable
####################################################################################################

# Python Standard Library Module Imports

import time
import random
import os
from datetime import datetime

# Python 3rd Party Library Module Imports
import ctypes
import win32api
import win32con
from prettytable import PrettyTable

####################################################################################################
# INSTRUCTIONS: Variables
#
# Set the TIMEOUT_VALUE below to how long the script will wait before moving mouse / keystroke
# NOTE: If you manually move the mouse or hit a key, this timer will reset, as designed.
#
# Set the BUSINESS_START value to when you want the script to start wiggling the mouse.
# Set the BUSINESS_END value to when you want the script to stop wiggling the mouse.
# The script will only perform functions between these times.
####################################################################################################

# countdown timer in seconds
TIMEOUT_VALUE = 240
COUNTDOWN_TIMER = TIMEOUT_VALUE

# business hours
BUSINESS_START = datetime.strptime("08:00:00", "%H:%M:%S").time()
BUSINESS_END = datetime.strptime("17:00:00", "%H:%M:%S").time()



# last input time
last_input_time = win32api.GetLastInputInfo()

# variable to track timestamps of when the ctrl key is pressed
last_ctrl_pressed_time = None

# a counter variable for the number of times the wiggle_mouse function is called
wiggle_count = 0


# create prettytable instances
business_hours_table = PrettyTable()
business_hours_table.title = "I'm here, Boss!"
business_hours_table.field_names = ["Idle Time", "Countdown", "Mouse Position", "Last Ctrl Press", "Wiggle Count"]

after_hours_table = PrettyTable()
after_hours_table.field_names = ["I'm away, Boss!"]
after_hours_table.align["Message"] = "l"
after_hours_table.max_width = 80


def wiggle_mouse():
    # generate random horizontal and vertical values
    h = random.randint(-50, 50)
    v = random.randint(-50, 50)
    
    # move the mouse cursor
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, h, v, 0, 0)
    
    # increment the wiggle count
    global wiggle_count
    wiggle_count += 1    
    
def press_ctrl_key():
    # press ctrl key three times with a 0.25 second delay
    for i in range(3):
        win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
        win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.25)


def print_mouse_position():
    x, y = win32api.GetCursorPos()
    return(f"({x}, {y})")

while True:
    # get the current time
    current_time = datetime.now().time()

    # clear the console
    os.system('cls')


    # check if the current time is within business hours
    if BUSINESS_START <= current_time <= BUSINESS_END:
        # calculate the idle time
        idle_time = '{:03d}'.format(int((win32api.GetTickCount() - last_input_time) / 1000))

        # format the countdown timer with 3 digits
        countdown_str = "{:03d}".format(COUNTDOWN_TIMER)
                
        
        # print the idle time, countdown timer, mouse position, and last Ctrl press, and wiggle count on the same line
        business_hours_table.clear_rows()
        business_hours_table.add_row([f"{idle_time} seconds", f"{countdown_str} seconds", print_mouse_position(), last_ctrl_pressed_time, wiggle_count])
        print(business_hours_table, end='\r')

        # check if the countdown timer has reached zero
        if COUNTDOWN_TIMER == 0:
            wiggle_mouse()
            press_ctrl_key()
            COUNTDOWN_TIMER = TIMEOUT_VALUE

        # check if the user has moved the mouse or pressed a key
        if win32api.GetLastInputInfo() != last_input_time:
            last_input_time = win32api.GetLastInputInfo()
            COUNTDOWN_TIMER = TIMEOUT_VALUE
        else:
            # decrement the countdown timer by 1 every second
            COUNTDOWN_TIMER -= 1
        
        # check if the Ctrl key is pressed
        if win32api.GetAsyncKeyState(win32con.VK_CONTROL) != 0:
            # set the current timestamp as the last pressed time
            last_ctrl_pressed_time = datetime.now().strftime("%H:%M:%S")
            
    
    else:

        # loop through the message, adding one character at a time and removing the last character to create a scrolling effect
        while not BUSINESS_START <= current_time <= BUSINESS_END:
            for i in range(86):
                os.system('cls')  # clear the console
                current_time = datetime.now().time()
                current_time_str = str(current_time)[:8]
                
                message = f"It's after hours. Current time: {current_time_str}. Script will resume at {BUSINESS_START}. "
                after_hours_table.clear_rows()
                after_hours_table.add_row([message[i:] + message[:i]])
                print(after_hours_table, end='\r')
                time.sleep(0.2)
            
                if BUSINESS_START <= current_time <= BUSINESS_END:
                    break     
    
            break
    
    # wait for 1 second before checking again
    time.sleep(1)
