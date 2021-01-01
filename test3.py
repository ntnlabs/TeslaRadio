#!/usr/bin/env python

import os
import sys
import time
from pathlib import Path
#from datetime import datetime

from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont

# Import the module and threading
from pyky040 import pyky040
import threading

# define variables
Volume = 0
Zmena = 1

# Define your callback
def my_callback_rotate(scale_position):
#    print('Hello world! The scale position is {}'.format(scale_position))
    global Volume
    global Zmena
    Volume = scale_position
    Zmena = 1

my_encoder = pyky040.Encoder(CLK=5, DT=6, SW=13)
my_encoder.setup(scale_min=0, scale_max=100, step=5, chg_callback=my_callback_rotate, sw_debounce_time=600)
my_thread = threading.Thread(target=my_encoder.watch)
my_thread.start()

if __name__ == "__main__":
    try:
        device = get_device()
        Zmena = 1
        while True:
            if (Zmena == 1):
                font_path1 = str(Path(__file__).resolve().parent.joinpath('fonts', 'C&C Red Alert [INET].ttf'))
                font_path2 = str(Path(__file__).resolve().parent.joinpath('fonts', 'DSEG7Modern-Regular.ttf'))

                font2_s = ImageFont.truetype(font_path1, 10)
                font2_m = ImageFont.truetype(font_path1, 18)
                font2_l = ImageFont.truetype(font_path1, 26)
                font2_xl = ImageFont.truetype(font_path2, 50)
#                Volume_str = str(Volume).rjust(3)
                with canvas(device) as draw:
                   draw.text((0,0), "Volume", font=font2_m, fill="white")
                   draw.text((80-(41*(len(str(Volume))-1)),30), str(Volume), font=font2_xl, fill="white")
                Zmena = 0
#            time.sleep(0.5)
# (x,y) x=doprava, y=dole
# black, blue, indigo, red, white

    except KeyboardInterrupt:
        pass
