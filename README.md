# imhereboss
An anti-idle script aimed to prevent Teams/Slack 'Away' status, screensaver, auto-screen lock, etc.

TLDR;
Run this script to:
* Prevent your screen from locking due to inactivity
* Always show your **Microsoft Teams**, **Slack**, or other communications software as 'Available'

## Purpose
A combination of inconveniences drove me to build this script:

- I work from home and am almost always at my computer during business hours.
- The screensaver + screen lock kicks in after 10 minutes of inactivity (domain GPO setting).
  - Local Admin privileges were removed and therefore we couldn't change it.
- **Microsoft Teams** and **Slack** won't allow you change the idle timer and sets your status to 'Away'
  - **Microsoft Teams** idle time is 5 minutes and **Slack** idle time is 10 minutes.

This causes issues when you spend long periods of time at your desk without keyboard/mouse activity:

- Reading a long article
- Writing notes on a physical notepad
- Being on a phone call
- Eating lunch at your desk (we all do this while WFH, right?)
- etc...

Doing any of the above and either the screen locks or your **Teams** + **Slack** shows 'Away'. So you keep having to wiggle your mouse.

I used to play an [extra long music video on YouTube][LYTV], but that only prevented the screen from locking.
**Microsoft Teams** + **Slack** would still set to 'Away' status. So I'd still have to wiggle my mouse every 5 minutes.

... and so I wrote this script to minimize the workarounds.

## Disclaimer
I'm a cyber security professional. What this script does is obviously a big no-no in the community. It is meant to be used responsibly (i.e., while at your computer). Don't have this script running while leaving your computer unattended. Don't run this script if your InfoSec policy prohibits it. You and only you are responsible for usage of this script.

## System Requirements
- The script currently works for Windows OS
- Python 3+
- Python 3rd party libraries:

```bash
  pip install pywin32
```
```bash
  pip install prettytable
```

## Usage

With the default values, this script will do the following:

* Keep track of the current idle time of the system.
* Countdown 4 minutes (240 seconds) to zero.
  * Default timer is set to 4 minutes because Microsoft Teams' idle timer is set to 5 minutes.
* If any mouse movement or keyboard stroke is detected, Idle Time resets to 0 and Countdown resets to 240.
  * This is to prevent the script from moving the mouse and pressing ctrl while you're working.
* Once the countdown reaches zero, the script will slightly move the mouse and hit the ctrl key.
* The countdown timer resets to 240 and the cycle continues.

The net result: Your screen will not lock and your **Microsoft Teams** + **Slack** will show you as 'Available'.

### Output:
Running the script will generate a PrettyTable with 5 columns:

```python
+-----------------------------------------------------------------------------+
|                               I'm here, Boss!                               |
+-------------+-------------+----------------+-----------------+--------------+
|  Idle Time  |  Countdown  | Mouse Position | Last Ctrl Press | Wiggle Count |
+-------------+-------------+----------------+-----------------+--------------+
| 097 seconds | 143 seconds |   (712, 147)   |     08:35:42    |      23      |
+-------------+-------------+----------------+-----------------+--------------+
```

* **Idle Time**: Current idle time on the OS. It resets if mouse movement or keyboard strokes are registered.
* **Countdown**: Time left before the automatic mouse movement and keyboard strokes are generated.
* **Mouse Position**: The current position of the mouse cursor on the screen.
* **Last Ctrl Press**: The time stamp of the ctrl key being pressed.
* **Wiggle Count**: The number of times the mouse was wiggled by the script




## Modifications

To modify the script there are 3 variables to tinker with:

Set the `TIMEOUT_VALUE` below to how long the script will wait before moving mouse / keystroke

Set the `BUSINESS_START` value to when you want the script to start wiggling the mouse.  
Set the `BUSINESS_END` value to when you want the script to stop wiggling the mouse.  
The script will only perform functions between these times.

```python
# countdown timer in seconds
TIMEOUT_VALUE = 240

# business hours
BUSINESS_START = datetime.strptime("08:00:00", "%H:%M:%S").time()
BUSINESS_END = datetime.strptime("17:00:00", "%H:%M:%S").time()
```

> Note: "Why business hours and after hours?", you ask.  
> "I thought you said use this script only when you are at your PC?".
> 
> You are correct. I used this as a failsafe in case someone forgets to stop the script before they step away from their computer.  
> _Once 'After Hours' kicks in, the script will stop moving the mouse and hitting the ctrl key, which in turn will allow your screen to lock and **Microsoft Teams** + **Slack** to show 'Away'._

[//]: # 

[LYTV]: https://www.youtube.com/watch?v=mM1dIwGO00w
