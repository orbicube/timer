import pyglet
import pathlib
import sys, os
from os import path

import datetime

from text_fix import ArcadeTextLayoutGroup

if getattr(sys, 'frozen', False):
    w_dir = pathlib.Path(sys._MEIPASS).parent
else:
    w_dir = os.path.dirname(os.path.abspath(__file__))

import tomllib
with open(path.join(w_dir, "settings.toml"), "rb") as f:
    settings = tomllib.load(f)
s_window = settings["window"]
s_timer = settings["timer"]

def clean_files(extra: str = None):
    files = ["add", "reset", "custom"]
    files.extend(s_timer["values"].keys())
    if extra:
        files.extend(extra)

    for f in files:
        if pathlib.Path(path.join(w_dir, f)).is_file():
            os.remove(path.join(w_dir, f))  


class Timer:

    def __init__(self):
        self.batch = pyglet.graphics.Batch()

        self.digits = []
        self.active = False

        if s_timer["resume"]:
            try:
                with open(path.join(w_dir, "current.txt")) as f:
                    str_time = f.read()
                self.seconds = sum(x * float(t) for x, t in zip([1, 60, 3600], reversed(str_time.split(":"))))
            except:
                self.seconds = float(s_timer["seconds"])
        else:
            self.seconds = float(s_timer["seconds"])

        for i in range(0,2):
            for j in range(0,4):
                self.digits.append(pyglet.text.Label(
                    '0', x=300*j, y=600-(i*400), width=300,
                    font_name=settings["font"]["name"],
                    font_size=settings["font"]["size"],
                    align='center', anchor_y='center',
                    color=tuple(settings["font"]["color"]),
                    batch=self.batch))


    def update(self):

        # Cap at 9999:99:99 - it will still count above that just not show it
        if self.seconds > 35999999:
            disp_seconds = 35999999
        else:
            disp_seconds = int(self.seconds)

        with open(path.join(w_dir, "current.txt"), 'w') as f:
            tdelta = str(datetime.timedelta(seconds=self.seconds))
            if "." in tdelta:
                tdelta = tdelta[:-7]
            f.write(tdelta)

        # separate seconds into each digit
        minutes = disp_seconds // 60
        rem_seconds = disp_seconds - (minutes * 60)
        if s_timer["hours"]:
            hours = minutes // 60
            rem_minutes = minutes - (hours * 60)
            digit_list = [hours//1000, hours//100 % 100,
                hours//10 % 10, hours % 10,
                rem_minutes//10 % 10, rem_minutes % 10,
                rem_seconds // 10, rem_seconds % 10]
        else:
            digit_list = [minutes//100000,
                minutes//10000 % 10000, minutes//1000 % 1000,
                minutes//100 % 100, minutes//10 % 10, minutes % 10,
                rem_seconds//10, rem_seconds % 10]

        for i in range(0,8):
            self.digits[i].text = str(digit_list[i])

            if self.active:
                self.digits[i].color = settings["font"]["color"]
            else:
                self.digits[i].color = settings["font"]["inactive_color"]


class Window(pyglet.window.Window):

    def __init__(self):
        super().__init__(width=1200, height=800,
            vsync=False, caption="timer",
            style=f"{'transparent' if s_window['transparent'] else 'dialog'}")      

        pyglet.text.layout.TextLayout.group_class = ArcadeTextLayoutGroup

        self.timer = Timer()

        # run tick() every second
        pyglet.clock.schedule_interval(self.tick, 1)


    def tick(self, dt):
        if self.timer.active:
            if self.timer.seconds <= 0:
                self.timer.active = False
                os.remove(path.join(w_dir, "run"))

                if settings["alarm"]["enabled"]:
                    alarm = pyglet.media.load(
                        path.join(w_dir, settings["alarm"]["file"]))
                    alarm.play().volume = settings["alarm"]["volume"] 

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
            self.timer.seconds += s_timer["seconds"]

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

        if pathlib.Path(path.join(w_dir, "reset")).is_file():
            # Create new timer with settings
            self.timer = Timer()

            # Turn it off if it was on
            if pathlib.Path(path.join(w_dir, "run")).is_file():
                os.remove(path.join(w_dir, "run"))

        for v in s_timer["values"].keys():
            if pathlib.Path(path.join(w_dir, v)).is_file():
                with open(path.join(w_dir, v)) as f:
                    lines = []
                    for line in f:
                        lines.append(line)

                try:
                    add_time = float(lines[0]) * s_timer["values"][v]

                    if len(lines) > 1 and s_timer["multiplier"]:
                        try:
                            add_time *= float(lines[1])
                        except:
                            pass

                    self.timer.seconds += add_time
                except:
                    pass


        self.timer.update()
        self.timer.batch.draw()

        clean_files()

clean_files(extra="run")
window = Window()

if not s_window["transparent"]:
    pyglet.gl.glClearColor(
        s_window["bg_color"][0],
        s_window["bg_color"][1],
        s_window["bg_color"][2], 1)

pyglet.app.run(1/5)