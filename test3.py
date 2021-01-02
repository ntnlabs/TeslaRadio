#!/usr/bin/env python

import os
import sys
import time
from pathlib import Path
#from datetime import datetime

#from demo_opts import get_device
from luma.core import cmdline
from luma.core.render import canvas
from PIL import ImageFont

# Import the module and threading
from pyky040 import pyky040
import threading
import argparse

# define variables
Volume = 0
Zmena = 1
Description = "Radio Expres: DURAN DURAN - RIO"

# define display
Display_args = argparse.Namespace()
Display_args.backlight_active = "low"
Display_args.bgr = False
Display_args.block_orientation = 0
Display_args.config = None
Display_args.debug = False
Display_args.display = "ssd1327"
Display_args.duration = 0.01
Display_args.framebuffer = "diff_to_previous"
Display_args.framebuffer_device = "/dev/fd0"
Display_args.ftdi_device = "ftdi://::/1"
Display_args.gpio = None
Display_args.gpio_backlight = 18
Display_args.gpio_chip_select = 24
Display_args.gpio_data_command = 24
Display_args.gpio_mode = None
Display_args.gpio_reset = 25
Display_args.gpio_reset_hold_time = 0
Display_args.gpio_reset_release_time = 0
Display_args.h_offset = 0
Display_args.height = 128
Display_args.i2c_address = "0x3C"
Display_args.i2c_port = 1
Display_args.interface = "spi"
Display_args.inverse = False
Display_args.loop = 0
Display_args.max_frames = None
Display_args.mode = "RGB"
Display_args.num_segments = 4
Display_args.rotate = 2
Display_args.scale = 2
Display_args.spi_bus_speed = 8000000
Display_args.spi_cs_high = False
Display_args.spi_device = 0
Display_args.spi_port = 0
Display_args.spi_transfer_size = 4096
Display_args.transform = "scale2x"
Display_args.v_offset = 0
Display_args.width = 128

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
#        device = get_device()
        device = cmdline.create_device(Display_args)

        font_path1 = str(Path(__file__).resolve().parent.joinpath('fonts', 'C&C Red Alert [INET].ttf'))
        font_path2 = str(Path(__file__).resolve().parent.joinpath('fonts', 'DSEG7Modern-Regular.ttf'))
        font2_s = ImageFont.truetype(font_path1, 10)
        font2_m = ImageFont.truetype(font_path1, 18)
        font2_l = ImageFont.truetype(font_path1, 26)
        font2_xl = ImageFont.truetype(font_path2, 50)
        Zmena = 1
        while True:
            if (Zmena == 1):
                with canvas(device) as draw:
                   draw.text((0,0), "Volume", font=font2_m, fill="white")
                   draw.text((80-(41*(len(str(Volume))-1)),30), str(Volume), font=font2_xl, fill="white")
                Zmena = 0
#            time.sleep(0.5)
# (x,y) x=doprava, y=dole
# black, blue, indigo, red, white

    except KeyboardInterrupt:
        pass
