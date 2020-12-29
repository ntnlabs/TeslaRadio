# Import the module and threading
from pyky040 import pyky040
import threading
import time

# define variables
Volume = 0
Menu_pos = 0

# Define your callback
def my_callback_rotate(scale_position):
#    print('Hello world! The scale position is {}'.format(scale_position))
    global Volume
    Volume = scale_position

def my_callback_press(state):
#    print('Hello world! The button has been pressed {}'.format(state))
    global Menu_pos
    Menu_pos = 1

my_encoder = pyky040.Encoder(CLK=5, DT=6, SW=13)
my_encoder.setup(scale_min=0, scale_max=100, step=1, chg_callback=my_callback_rotate, sw_callback=my_callback_press, sw_debounce_time=300)
my_thread = threading.Thread(target=my_encoder.watch)
my_thread.start()

# Do other stuff
print('Display Init')
while True:
    print('--------------------')
    print('|                  |')
    print('|      {:<3}       |'.format(Volume))
    print('|                  |')
    print('--------------------')

    time.sleep(100)
