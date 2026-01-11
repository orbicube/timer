import pyglet
import pathlib
import sys, os
from os import path

if getattr(sys, 'frozen', False):
    w_dir = pathlib.Path(sys._MEIPASS).parent
else:
    w_dir = os.path.dirname(os.path.abspath(__file__))

import tomllib
with open(path.join(w_dir, "settings.toml"), "rb") as f:
    settings = tomllib.load(f)

class Timer:

    def __init__(self):
        self.batch = pyglet.graphics.Batch()

        self.digits = []
        self.active = False
        self.seconds = settings["timer"]["seconds"]

        for i in range(0,5):
            self.digits.append(pyglet.text.Label(
                '0', x=300*i, y=200, width=300,
                font_name=settings["font"]["name"],
                font_size=settings["font"]["size"],
                align='center', anchor_y='center',
                color=tuple(settings["font"]["color"]),
                batch=self.batch))

    def update(self):

        # Cap at 999:59 - it will still count above that just not show it
        if self.seconds > 59999:
            disp_seconds = 59999
        else:
            disp_seconds = self.seconds

        # separate seconds into each digit
        minutes = disp_seconds // 60
        rem_seconds = disp_seconds - (minutes * 60)
        digit_list = [minutes//100, minutes//10 % 10, minutes % 10,
            rem_seconds//10, rem_seconds % 10]

        for i in range(0,5):
            self.digits[i].text = str(digit_list[i])

            if self.active:
                self.digits[i].color = settings["font"]["color"]
            else:
                self.digits[i].color = settings["font"]["inactive_color"]


class Window(pyglet.window.Window):

    def __init__(self):
        super().__init__(width=1500, height=400, vsync=False,
            caption="timer", style='transparent')      

        self.timer = Timer()

        # run tick() every second
        pyglet.clock.schedule_interval(self.tick, 1)


    def tick(self, dt):
        if self.timer.active:
            if self.timer.seconds <= 0:
                self.timer.active = False
                os.remove(path.join(w_dir, "run"))
            else:  
                self.timer.seconds -= 1

            self.timer.update()


    def on_draw(self):
        self.clear()

        if pathlib.Path(path.join(w_dir, "run")).is_file():
            self.timer.active = True
        else:
            self.timer.active = False

        if pathlib.Path(path.join(w_dir, "add")).is_file():
            self.timer.seconds += settings["timer"]["seconds"]

            os.remove(path.join(w_dir, "add"))  

        if pathlib.Path(path.join(w_dir, "custom")).is_file():
            with open(path.join(w_dir, "custom")) as f:
                # If file doesn't have an integer in it, just ignore it
                try:
                    self.timer.seconds += int(f.readline())
                except:
                    pass

                # Since you can remove time this way, stop it if it's under 1
                if self.timer.seconds <= 0:
                    self.timer.seconds = 0

            os.remove(path.join(w_dir, "custom"))  

        if pathlib.Path(path.join(w_dir, "reset")).is_file():
            # Create new timer with settings
            self.timer = Timer()

            os.remove(path.join(w_dir, "reset"))

            # Turn it off if it was on
            if pathlib.Path(path.join(w_dir, "run")).is_file():
                os.remove(path.join(w_dir, "run"))

        self.timer.update()
        self.timer.batch.draw()

if pathlib.Path(path.join(w_dir, "run")).is_file():
    os.remove(path.join(w_dir, "run"))  
if pathlib.Path(path.join(w_dir, "add")).is_file():
    os.remove(path.join(w_dir, "add"))
if pathlib.Path(path.join(w_dir, "reset")).is_file():
    os.remove(path.join(w_dir, "reset"))
if pathlib.Path(path.join(w_dir, "custom")).is_file():
    os.remove(path.join(w_dir, "custom"))
window = Window()
pyglet.app.run(1/5)