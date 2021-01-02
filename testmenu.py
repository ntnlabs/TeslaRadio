#!/usr/bin/env python

from time import sleep
from pathlib import Path
from luma.core import cmdline
from luma.core.render import canvas
from PIL import ImageFont
from random import randrange
from pyky040 import pyky040 # this module was forked/changed
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
Changed = 1
Menu_menu = [['Volume', 'Play', 'Setup', 'Config', 'Exit'],['Play/pause', 'Stop', 'Next', 'Previous'],['Enable SSH', 'Enable BT', 'Enable Wifi' ],['Shutdown', 'Reboot']]
Screensaver = 0
Timeout = 0
Where = 0

# Define your callback
def rotate_up(scale_position):
    global Changed, Timeout
    Changed = 1
    Timeout = 0

def rotate_down(scale_position):
    global Changed, Timeout
    Changed = 1
    Timeout = 0

def rotate_press(state):
#    print('Hello world! The button has been pressed {}'.format(state))
    global Changed, Timeout
    Changed = 1
    Timeout = 0

def Update_Screen(device):
    global Changed, Menu_menu, Screensaver

    if (Where == 0):
        with canvas(device) as draw:
            draw.text((10,40), Menu_menu[0][0], font = font2_ll, fill = "white")
    else:
        with canvas(device) as draw:
            draw.text((10,20), Menu_menu[0][0], font = font2_l, fill = "white")
            draw.text((1,40), Menu_menu[1][1], font = font2_ll, fill = "white")
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
            sleep(0.1)
            if (Screensaver == 0):
                if ( Timeout < Timeout_max ):
                    Timeout = Timeout + 1
                else:
                    Timeout = 0
                    Where = 0
                    Changed = 1
                    Screensaver = 1
            else:
                if ( Timeout < (Timeout_max * 2) ):
                    Timeout = Timeout + 1
                else:
                    Timeout = 0
                    Where = 0
                    Changed = 1

#            time.sleep(0.5)
# (x,y) x=doprava, y=dole
# black, blue, indigo, red, white

    except KeyboardInterrupt:
        pass
