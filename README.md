# timer
pyglet countdown timer.
## Installation
### Python (3.11+)
```
  python -m pip install pyglet
  python timer.py
```
### Windows
Run the standalone .exe from [Releases](https://github.com/orbicube/timer/releases/latest).
## Usage
* To start the timer, create a file called "run" in the directory. Deleting it will pause the timer.
* To add the starting value back onto the timer, create a file called "add" in the directory.
* To reset the timer, create a file called "reset" in the directory.
* To add (or remove with - in front) a custom amount of time, create a file called "custom" to the directory with a text value of the amount of seconds to add
* For Windows users there are .bat files to trigger these with a Stream Deck or similar application.
* To use in OBS, create a separate game capture of the program for each digit and crop. The window is 1500px wide, so 0-300, 300-600, etc.
  
## Configuration
settings.toml is configurable. 
### Reference
```
[timer]
seconds: Integer # How long to run the timer for, and how much will be added with the "add" command

[font]
name: String # Font name installed on the system
font: Integer # Font size, too large may crash; Arial can go up to 340 whereas Comic Sans MS is good up to 270
color: Array # RGB integer array for colour to use while counting down
inactive_color: Array # RGB integer array for colour to use while inactive

[alarm]
enabled: Boolean
file: String # File name, likely WAV only
volume: Float # 1.0 = 100%

```
