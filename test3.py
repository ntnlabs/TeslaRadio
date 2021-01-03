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
import os

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
Volume_step = 0.5
Volume_max = 100
Changed = 1
Menu_menu = ['Play', 'Setup', 'Config', 'Exit']
Menu_submenu = [['Play/pause', 'Stop', 'Next', 'Previous'],['Screensaver', 'Input', 'Timeout', 'Language', 'Update'],['Enable SSH', 'Enable BT', 'Enable Wifi' ],['Shutdown', 'Reboot']]
Menu_uroven = 0
Menu_menu_pointer = 0
Menu_submenu_pointer = 0
Menu_parent = 0
Song_description = "Radio Expres: DURAN DURAN - RIO" # demo/test desc
Timeout = 0
Timeout_max = 60
Screensaver = 0

# Define your callback
def rotate_up(scale_position):
    global Volume, Changed, Timeout, Screensaver, Menu_uroven, Menu_menu_pointer, Menu_submenu_pointer, Menu_parent
    if (Screensaver > 0):
        Screensaver = 0
        Changed = 1
        Timeout = 0
        return
    if (Menu_uroven == 0):
        if (Volume < Volume_max):
            Volume = Volume + Volume_step
    elif (Menu_uroven == 1):
        if (Menu_menu_pointer < len(Menu_menu[Menu_menu_pointer])-1):
            Menu_menu_pointer = Menu_menu_pointer + 1
    elif (Menu_uroven == 2):
        if (Menu_submenu_pointer < len(Menu_submenu[Menu_parent])-1):
            Menu_submenu_pointer = Menu_submenu_pointer + 1
    Changed = 1
    Timeout = 0

def rotate_down(scale_position):
    global Volume, Changed, Timeout, Screensaver, Menu_uroven, Menu_menu_pointer, Menu_submenu_pointer, Menu_parent
    if (Screensaver > 0):
        Screensaver = 0
        Changed = 1
        Timeout = 0
        return
    if (Menu_uroven == 0):
        if (Volume > 0):
            Volume = Volume - Volume_step
    if (Menu_uroven == 1):
        if (Menu_menu_pointer > 0):
            Menu_menu_pointer = Menu_menu_pointer - 1
    elif (Menu_uroven == 2):
        if (Menu_submenu_pointer > 0):
            Menu_submenu_pointer = Menu_submenu_pointer - 1
    Changed = 1
    Timeout = 0

def rotate_press(state):
    global Volume, Changed, Timeout, Screensaver, Menu_uroven, Menu_menu_pointer, Menu_submenu_pointer, Menu_parent
    if ( state == "UP" ):
        if (Screensaver > 0):
            Screensaver = 0
            Changed = 1
            Timeout = 0
            return
        if (Menu_uroven < 2):
            Menu_uroven = Menu_uroven + 1
            Menu_submenu_pointer = 0
            Menu_parent = Menu_menu_pointer
        else:
            if ((Menu_menu_pointer == 3) and (Menu_submenu_pointer == 1)):
                os.system("poweroff")
                Menu_menu_pointer = 0
                Menu_submenu_pointer = 0
                Menu_parent = 0
                Menu_uroven = 0
                return
            if ((Menu_menu_pointer == 3) and (Menu_submenu_pointer == 0)):
                os.system("reboot")
                Menu_menu_pointer = 0
                Menu_submenu_pointer = 0
                Menu_parent = 0
                Menu_uroven = 0
                return
            Menu_uroven = 1
            Menu_menu_pointer = Menu_parent
    Changed = 1
    Timeout = 0

def init_stars(num_stars, max_depth):
    stars = []
    for i in range(num_stars):
        star = [randrange(-25, 25), randrange(-25, 25), randrange(1, max_depth)]
        stars.append(star)
    return stars


def move_and_draw_stars(stars, max_depth):
    origin_x = device.width // 2
    origin_y = device.height // 2

    with canvas(device) as draw:
        for star in stars:
            star[2] -= 0.19

            if star[2] <= 0:
                star[0] = randrange(-25, 25)
                star[1] = randrange(-25, 25)
                star[2] = max_depth

            k = 128.0 / star[2]
            x = int(star[0] * k + origin_x)
            y = int(star[1] * k + origin_y)

            if 0 <= x < device.width and 0 <= y < device.height:
                size = (1 - float(star[2]) / max_depth) * 4
                shade = "white"
                if (device.mode == "RGB"):
                    color = int(100 + (1 - float(star[2]) / max_depth) * 155)
                    if (color < 150):
                        shade = "blue"
                    elif (color < 180):
                        shade = "indigo"
                    elif (color < 210):
                        shade = "red"
                    elif (color < 240):
                        shade = "white"
                else:
                    shade = "white"
                draw.rectangle((x, y, x + size, y + size), fill = shade)


def Update_Screen(device):
    global Changed, Screensaver, Menu_uroven, Menu_menu_pointer, Menu_submenu_pointer, Menu_parent

    with canvas(device) as draw:
        if (Menu_uroven == 0):
            if (Screensaver > 0):
                draw.text((0,0), "Volume", font = font2_m, fill = "blue")
                draw.text((80-(41*(len(str(int(Volume)))-1)),30), str(int(Volume)), font = font2_xl, fill = "blue")
            else:
                draw.text((0,0), "Volume", font = font2_m, fill = "white")
                draw.text((80-(41*(len(str(int(Volume)))-1)),30), str(int(Volume)), font = font2_xl, fill = "red")
        elif (Menu_uroven == 1):
            draw.text((10,40), Menu_menu[Menu_menu_pointer], font = font2_ll, fill = "white")
        elif (Menu_uroven == 2):
            draw.text((10,20), Menu_menu[Menu_parent], font = font2_l, fill = "white")
            draw.text((1,40), Menu_submenu[Menu_parent][Menu_submenu_pointer], font = font2_ll, fill = "white")
    Changed = 0

# threading the encoder
my_encoder = pyky040.Encoder(CLK=5, DT=6, SW=13)
my_encoder.setup(scale_min=0, scale_max=100, step=5, inc_callback=rotate_up, dec_callback=rotate_down, sw_callback=rotate_press, sw_debounce_time=1200)
my_thread = threading.Thread(target=my_encoder.watch)
my_thread.start()

if __name__ == "__main__":
    try:
        device = cmdline.create_device(Display_args)
        font_path1 = str(Path(__file__).resolve().parent.joinpath('fonts', 'C&C Red Alert [INET].ttf'))
        font_path2 = str(Path(__file__).resolve().parent.joinpath('fonts', 'DSEG7Modern-Regular.ttf'))
        font_path3 = str(Path(__file__).resolve().parent.joinpath('fonts', 'Volter__28Goldfish_29.ttf'))
        font2_m = ImageFont.truetype(font_path3, 9)
        font2_l = ImageFont.truetype(font_path1, 18)
        font2_ll = ImageFont.truetype(font_path1, 28)
        font2_xl = ImageFont.truetype(font_path2, 50)
        Zmena = 1

        while True:
            if (Changed == 1):
                Update_Screen(device)
            sleep(0.05)
            if (Screensaver == 0):
                if ( Timeout < Timeout_max ):
                    Timeout = Timeout + 1
                else:
                    if (Menu_uroven == 0):
                        Screensaver = 1
                    Timeout = 0
                    Changed = 1
                    Menu_uroven = 0
                    Menu_menu_pointer = 0
                    Menu_submenu_pointer = 0
                    Menu_parent = 0
            elif (Screensaver == 1):
                if ( Timeout < (Timeout_max * 2) ):
                    Timeout = Timeout + 1
                else:
                    Timeout = 0
                    Changed = 1
                    Screensaver = 2
                    max_depth = 32
                    stars = init_stars(512, max_depth)
            elif (Screensaver == 2):
                move_and_draw_stars(stars, max_depth)


#            time.sleep(0.5)
# (x,y) x=doprava, y=dole
# black, blue, indigo, red, white

    except KeyboardInterrupt:
        pass
