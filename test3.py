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

# define display
Display_args = argparse.Namespace()
Display_args.backlight_active = "low"
Display_args.bgr = False # not for ssd1327
Display_args.block_orientation = 0
Display_args.config = None
Display_args.debug = False
Display_args.display = "ssd1327"
Display_args.duration = 0.01
Display_args.framebuffer = "diff_to_previous"
Display_args.framebuffer_device = "/dev/fd0"
Display_args.ftdi_device = "ftdi://::/1"
Display_args.gpio = None
Display_args.gpio_backlight = 17 # not for ssd1327
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

# define variables
Volume = 0
Volume_step = 5
Volume_max = 100
Changed = 1
Command = 0
Menu = 0
Submenu = 0
Where = 0
Menu_menu = [['Volume', 'Play', 'Setup', 'Config', 'Exit'],['Play/pause', 'Stop', 'Next', 'Previous'],['Enable SSH', 'Enable BT', 'Enable Wifi' ],['Shutdown', 'Reboot']]
Song_description = "Radio Expres: DURAN DURAN - RIO" # demo/test desc
Timeout = 0
Timeout_max = 30

# Define your callback
def rotate_up(scale_position):
#    print('Hello world! The scale position is {}'.format(scale_position))
    global Volume, Changed, Menu, Submenu, Where, Timeout
    if (Menu == 0):
        if (Volume < Volume_max):
            Volume = Volume + Volume_step
    elif (Where == 0):
        if (Menu < (len(Menu_menu[0])-1)):
            Menu = Menu + 0.5
            Where = 0
    elif (Submenu < (len(Menu_menu[int(Menu)])-1)):
        Submenu = Submenu + 0.5
    Changed = 1
    Timeout = 0

def rotate_down(scale_position):
#    print('Hello world! The scale position is {}'.format(scale_position))
    global Volume, Changed, Menu, Submenu, Where, Timeout
    if (Menu == 0):
        if (Volume > 0):
            Volume = Volume - Volume_step
    elif (Where == 0):
        if (Menu > 1):
            Menu = Menu - 0.5
            Where = 0
    elif (Submenu > 0):
        Submenu = Submenu - 0.5
    Changed = 1
    Timeout = 0

def rotate_press(state):
#    print('Hello world! The button has been pressed {}'.format(state))
    global Menu, Submenu, Changed, Where, Timeout
    if ( state == "UP" ):
        if (Menu == 0):
            Menu = 1
            Where = 0
            Submenu = 0
        else:
            if (Where == 0):
                Submenu = 0
                Where = Menu
            else:
                Where = 0
                Submenu = 0
    Changed = 1
    Timeout = 0

def Update_Screen(device):
    global Changed, Menu, Menu_menu, Where



    if ((Menu == 0) & (Where == 0)):
        with canvas(device) as draw:
            draw.text((0,0), "Volume", font=font2_m, fill="white")
            draw.text((80-(41*(len(str(int(Volume)))-1)),30), str(int(Volume)), font=font2_xl, fill="white")
    elif (Where == 0):
        with canvas(device) as draw:
            draw.text((10,40), Menu_menu[0][int(Menu)], font=font2_ll, fill="white")
    elif (Where != 0):
        with canvas(device) as draw:
            draw.text((10,20), Menu_menu[0][int(Menu)], font=font2_l, fill="white")
            draw.text((1,40), Menu_menu[int(Menu)][int(Submenu)], font=font2_ll, fill="white")
    Changed = 0

# threading the encoder
my_encoder = pyky040.Encoder(CLK=5, DT=6, SW=13)
my_encoder.setup(scale_min=0, scale_max=100, step=5, inc_callback=rotate_up, dec_callback=rotate_down, sw_callback=rotate_press, sw_debounce_time=600)
my_thread = threading.Thread(target=my_encoder.watch)
my_thread.start()

if __name__ == "__main__":
    try:
        device = cmdline.create_device(Display_args)
        font_path1 = str(Path(__file__).resolve().parent.joinpath('fonts', 'C&C Red Alert [INET].ttf'))
        font_path2 = str(Path(__file__).resolve().parent.joinpath('fonts', 'DSEG7Modern-Regular.ttf'))
        font2_m = ImageFont.truetype(font_path1, 18)
        font2_l = ImageFont.truetype(font_path1, 22)
        font2_ll = ImageFont.truetype(font_path1, 36)
        font2_xl = ImageFont.truetype(font_path2, 50)
        Zmena = 1

        while True:
            if (Changed == 1):
                Update_Screen(device)
            time.sleep(0.1)
            if ( Timeout < Timeout_max ):
                Timeout = Timeout + 1
            else:
                Timeout = 0
                Menu = 0
                Submenu = 0
                Where = 0
                Changed = 1

#            time.sleep(0.5)
# (x,y) x=doprava, y=dole
# black, blue, indigo, red, white

    except KeyboardInterrupt:
        pass
