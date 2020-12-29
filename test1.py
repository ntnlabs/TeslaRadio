# Import the module and threading
from pyky040 import pyky040
import threading
import time

# Define your callback
def my_callback_rotate(scale_position):
    print('Hello world! The scale position is {}'.format(scale_position))

def my_callback_press(state):
    print('Hello world! The button has been pressed {}'.format(state))

# Init the encoder pins
my_encoder = pyky040.Encoder(CLK=5, DT=6, SW=13)

# Or the encoder as a device (must be installed on the system beforehand!)
# my_encoder = pyky040.Encoder(device='/dev/input/event0')

# Setup the options and callbacks (see documentation)
my_encoder.setup(scale_min=0, scale_max=100, step=1, chg_callback=my_callback_rotate, sw_callback=my_callback_press, sw_debounce_time=300)

# Create the thread
my_thread = threading.Thread(target=my_encoder.watch)

# Launch the thread
my_thread.start()

# Do other stuff
print('Other stuff...')
while True:
    print('Looped stuff...')
    time.sleep(1000)
# ... this is also where you can setup other encoders!
