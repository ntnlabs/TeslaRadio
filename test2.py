# Import the module and threading
from pyky040 import pyky040
import threading
from time import sleep, time

# define variables
Volume = 0
Volume_prev = 11
Menu_pos = 0
Menu_pos_prev = 0
Menu = ['Volume', 'Next', 'Stop', 'MP3', 'Settings']
Timeout = 0
Long_press = 1000
Sw_down_time = 0

# Define your callback
def my_callback_rotate(scale_position):
#    print('Hello world! The scale position is {}'.format(scale_position))
    global Volume
    Volume = str(scale_position)

def my_callback_press(state):
#    print('Hello world! The button has been pressed {}'.format(state))
    global Menu_pos
    global Long_press
    global Sw_down_time
    if ( state == "DOWN" ):
        Sw_down_time = time() * 1000
    elif ( state == "UP" ):
        if ( ( (time() * 1000) - Sw_down_time ) > Long_press ):
            Menu_pos = 4
        elif ( Menu_pos < 3 ):
            Menu_pos = Menu_pos + 1
        else:
            Menu_pos = 1

my_encoder = pyky040.Encoder(CLK=5, DT=6, SW=13)
my_encoder.setup(scale_min=0, scale_max=100, step=1, chg_callback=my_callback_rotate, sw_callback=my_callback_press, sw_debounce_time=600)
my_thread = threading.Thread(target=my_encoder.watch)
my_thread.start()

# Do other stuff
# print('Display Init',Volume)
while True:
    if (Menu_pos == 0):
        if ( Volume != Volume_prev ):
            print('--------------------')
            print('| {:>8}         |'.format(Menu[Menu_pos]))
            print('|       {:>3}        |'.format(Volume))
            print('|                 {}|'.format(Menu_pos))
            print('--------------------')
            Volume_prev = Volume
            Menu_pos_prev = 0
            Timeout = 0

    if ( Menu_pos != Menu_pos_prev ):
        print('--------------------')
        print('|                  |')
        print('|     {:>8}     |'.format(Menu[Menu_pos]))
        print('|                 {}|'.format(Menu_pos))
        print('--------------------')
        Menu_pos_prev = Menu_pos
        Timeout = 0

# cakame chvilku
    sleep(0.1)

# back to default
    if ( Timeout < 60 ):
        Timeout = Timeout + 1
    else:
        Timeout = 0
        Menu_pos = 0
