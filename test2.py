# Import the module and threading
from pyky040 import pyky040
import threading
import time

# define variables
Volume = 0
Volume_prev = 11
Menu_pos = 0
Menu_pos_prev = 0
Menu = ['Volume', 'Next', 'Stop', 'Settings']

# Define your callback
def my_callback_rotate(scale_position):
#    print('Hello world! The scale position is {}'.format(scale_position))
    global Volume
    Volume = str(scale_position)

def my_callback_press(state):
#    print('Hello world! The button has been pressed {}'.format(state))
    global Menu_pos
    if ( Menu_pos < 3 ):
        Menu_pos = Menu_pos + 1
    else:
        Menu_pos = 1

my_encoder = pyky040.Encoder(CLK=5, DT=6, SW=13)
my_encoder.setup(scale_min=0, scale_max=100, step=1, chg_callback=my_callback_rotate, sw_callback=my_callback_press, sw_debounce_time=1000)
my_thread = threading.Thread(target=my_encoder.watch)
my_thread.start()

# Do other stuff
print('Display Init',Volume)
while True:
    if (Menu_pos == 0):
        if ( Volume != Volume_prev ):
            print('--------------------')
            print('| {:>8}         |'.format(Menu[Menu_pos]))
            print('|       {:>3}        |'.format(Volume))
            print('|                 {}|'.format(Menu_pos))
            print('--------------------')
            Volume_prev = Volume

    if ( Menu_pos != Menu_pos_prev ):
        print('--------------------')
        print('|                  |'.format(Menu[Menu_pos]))
        print('|     {:>8}     |'.format(Volume))
        print('|                 {}|'.format(Menu_pos))
        print('--------------------')
        Menu_pos_prev = Menu_pos

# cakame chvilku
    time.sleep(0.1)
