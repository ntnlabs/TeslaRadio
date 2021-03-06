#!/usr/bin/env python

from time import sleep
from pathlib import Path
from luma.core import cmdline
from luma.core.render import canvas
from luma.core.virtual import viewport
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
Menu_menu = ['Player', 'Setup', 'Config', 'Exit']
Menu_submenu = [['Play/pause', 'Stop', 'Next', 'Previous'],['Screensaver', 'Input', 'Timeout', 'Language', 'Update'],['Enable SSH', 'Enable BT', 'Enable Wifi' ],['Shutdown', 'Reboot']]
Menu_uroven = 0
Menu_menu_pointer = 0
Menu_submenu_pointer = 0
Menu_parent = 0
Song_description = "Radio Radio Expres Expres: GLADIATOR GLADIATOR GLADIATOR - NECHCEM OOOO TEBAAA PRIIIST"  # demo/test desc
Timeout = 0
Timeout_max = 120 # x/2 = seconds
Screensaver = 0
Station_name = ""
Artist_name = ""
Song_name = ""
State = ""
Scroll_timer = 0
Scroll_timer_max = 5
Scroll_index_Song = 0
Scroll_need_Song = 0
Scroll_direction_Song = 1
Song_name_scrolling = ""
Scroll_display_len_Song = 10

# Break song data into Station/Artist/Song (other stations may broadcast different way - TODO: check/split byt station)
def New_song(Description):
    global Station_name, Song_name, Artist_name
    Station_name, Song_name = Description.split(":")
    Station_name = Station_name.strip()
    Artist_name, Song_name = Song_name.split("-")
    Artist_name = Artist_name.strip()
    Song_name = Song_name.strip()

# rotate button up
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
        if (Menu_menu_pointer < len(Menu_menu[int(Menu_menu_pointer)])-1):
            Menu_menu_pointer = Menu_menu_pointer + 0.5
    elif (Menu_uroven == 2):
        if (Menu_submenu_pointer < len(Menu_submenu[int(Menu_parent)])-1):
            Menu_submenu_pointer = Menu_submenu_pointer + 0.5
    Changed = 1
    Timeout = 0

# rotate button down
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
            Menu_menu_pointer = Menu_menu_pointer - 0.5
    elif (Menu_uroven == 2):
        if (Menu_submenu_pointer > 0):
            Menu_submenu_pointer = Menu_submenu_pointer - 0.5
    Changed = 1
    Timeout = 0

# rotate button pressed (my KY040 module!!!)
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
            if ((Menu_menu_pointer == 3) and (Menu_submenu_pointer == 0)):
# run as sudo
                os.system("poweroff")
                Menu_menu_pointer = 0
                Menu_submenu_pointer = 0
                Menu_parent = 0
                Menu_uroven = 0
                return
            if ((Menu_menu_pointer == 3) and (Menu_submenu_pointer == 1)):
# run as sudo
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

# needed for screensaver
def init_stars(num_stars, max_depth):
    stars = []
    for i in range(num_stars):
        star = [randrange(-25, 25), randrange(-25, 25), randrange(1, max_depth)]
        stars.append(star)
    return stars

# screensaver
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

# main drawing loop
def Update_Screen(device):
    global Changed, Screensaver, Menu_uroven, Menu_menu_pointer, Menu_submenu_pointer, Menu_parent

    if (Screensaver > 0):
        MyColor = "blue"
    else:
        MyColor = "red"

    with canvas(device) as draw:
        if ( State == "Playing" ):
            draw.text((128-(len(State)*5),0), State, font = font2_s, fill = MyColor)
            draw.text((0,98), "Station: " + Station_name_scrolling, font = font2_s, fill = MyColor)
            draw.text((0,108), "Artist: " + Artist_name_scrolling, font = font2_s, fill = MyColor)
            draw.text((0,118), "Song: " + Song_name_scrolling, font = font2_s, fill = MyColor)
        if (Menu_uroven == 0):
            draw.text((0,0), "Volume", font = font2_s, fill = MyColor)
            draw.text((80-(41*(len(str(int(Volume)))-1)),30), str(int(Volume)), font = font2_xl, fill = MyColor)
        elif (Menu_uroven == 1):
            draw.text((10,40), Menu_menu[int(Menu_menu_pointer)], font = font2_ll, fill = "white")
        elif (Menu_uroven == 2):
            draw.text((10,20), Menu_menu[int(Menu_parent)], font = font2_l, fill = "white")
            draw.text((1,40), Menu_submenu[int(Menu_parent)][int(Menu_submenu_pointer)], font = font2_ll, fill = "white")

    Changed = 0

# threading the encoder
my_encoder = pyky040.Encoder(CLK=5, DT=6, SW=13)
my_encoder.setup(scale_min=0, scale_max=100, step=5, inc_callback=rotate_up, dec_callback=rotate_down, sw_callback=rotate_press, sw_debounce_time=1200)
my_thread = threading.Thread(target=my_encoder.watch)
my_thread.start()

if __name__ == "__main__":
    try:
# initialise all
        device = cmdline.create_device(Display_args)
        font_path1 = str(Path(__file__).resolve().parent.joinpath('fonts', 'C&C Red Alert [INET].ttf'))
        font_path2 = str(Path(__file__).resolve().parent.joinpath('fonts', 'DSEG7Modern-Regular.ttf'))
        font_path3 = str(Path(__file__).resolve().parent.joinpath('fonts', 'Volter__28Goldfish_29.ttf'))
        font2_s = ImageFont.truetype(font_path3, 9)
        font2_l = ImageFont.truetype(font_path1, 18)
        font2_ll = ImageFont.truetype(font_path1, 28)
        font2_xl = ImageFont.truetype(font_path2, 50)
        Zmena = 1
        State = "Playing"
        
# scrolling engine
        New_song(Song_description)
        Scroll_timer = 99
        Scroll_timer_max = 12
        Scroll_index_Song = 0
        Scroll_direction_Song = 1
        Scroll_direction_temp_Song = 0
        Scroll_index_Artist = 0
        Scroll_direction_Artist = 1
        Scroll_direction_temp_Artist = 0
        Scroll_index_Station = 0
        Scroll_direction_Station = 1
        Scroll_direction_temp_Station = 0
        Scroll_buffer_max = 5
        Scroll_buffer_Song = Scroll_buffer_max
        Scroll_buffer_Artist = Scroll_buffer_max
        Scroll_buffer_Station = Scroll_buffer_max
        Scroll_display_len_Song = 16
        Scroll_display_len_Artist = 15
        Scroll_display_len_Station = 14
        Artist_name_scrolling = Artist_name[0:Scroll_display_len_Artist]
        Song_name_scrolling = Song_name[0:Scroll_display_len_Song]
        Station_name_scrolling = Station_name[0:Scroll_display_len_Station]
        Scroll_need_Song = len(Song_name) - Scroll_display_len_Song
        Scroll_need_Artist = len(Artist_name) - Scroll_display_len_Artist
        Scroll_need_Station = len(Station_name) - Scroll_display_len_Station

        if ( (Scroll_need_Song > 0) or (Scroll_need_Artist > 0) or (Scroll_need_Station > 0)):
            Wanna_scroll = True
        else:
            Wanna_scroll = False
# main loop
        while True:
            if ( Wanna_scroll == True and (Screensaver == 0 or Screensaver == 1) ):
                if ( Scroll_timer < Scroll_timer_max ):
                    Scroll_timer = Scroll_timer + 1
                else:
                    if ( Scroll_need_Song > 0 ):
                        Song_name_scrolling = Song_name[0+Scroll_index_Song:Scroll_display_len_Song+Scroll_index_Song]
                        Scroll_index_Song = Scroll_index_Song + Scroll_direction_Song
                        if ( (Scroll_index_Song == 0) or (Scroll_index_Song == Scroll_need_Song) ):
                            if ( Scroll_buffer_Song > 0 ):
                                if ( Scroll_direction_temp_Song == 0 ):
                                    Scroll_direction_temp_Song = Scroll_direction_Song
                                    Scroll_direction_Song = 0
                                Scroll_buffer_Song = Scroll_buffer_Song - 1
                            else:
                                Scroll_direction_Song = Scroll_direction_temp_Song * -1
                                Scroll_direction_temp_Song = 0
                                Scroll_buffer_Song = Scroll_buffer_max

                    if ( Scroll_need_Artist > 0 ):
                        Artist_name_scrolling = Artist_name[0+Scroll_index_Artist:Scroll_display_len_Artist+Scroll_index_Artist]
                        Scroll_index_Artist = Scroll_index_Artist + Scroll_direction_Artist
                        if ( (Scroll_index_Artist == 0) or (Scroll_index_Artist == Scroll_need_Artist) ):
                            if ( Scroll_buffer_Artist > 0 ):
                                if ( Scroll_direction_temp_Artist == 0 ):
                                    Scroll_direction_temp_Artist = Scroll_direction_Artist
                                    Scroll_direction_Artist = 0
                                Scroll_buffer_Artist = Scroll_buffer_Artist - 1
                            else:
                                Scroll_direction_Artist = Scroll_direction_temp_Artist * -1
                                Scroll_direction_temp_Artist = 0
                                Scroll_buffer_Artist = Scroll_buffer_max

                    if ( Scroll_need_Station > 0 ):
                        Station_name_scrolling = Station_name[0+Scroll_index_Station:Scroll_display_len_Station+Scroll_index_Station]
                        Scroll_index_Station = Scroll_index_Station + Scroll_direction_Station
                        if ( (Scroll_index_Station == 0) or (Scroll_index_Station == Scroll_need_Station) ):
                            if ( Scroll_buffer_Station > 0 ):
                                if ( Scroll_direction_temp_Station == 0 ):
                                    Scroll_direction_temp_Station = Scroll_direction_Station
                                    Scroll_direction_Station = 0
                                Scroll_buffer_Station = Scroll_buffer_Station - 1
                            else:
                                Scroll_direction_Station = Scroll_direction_temp_Station * -1
                                Scroll_direction_temp_Station = 0
                                Scroll_buffer_Station = Scroll_buffer_max

                    Scroll_timer = 0
                    Changed = 1
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

    except KeyboardInterrupt:
        pass
    
