
"""
--------------------------------------------------------------------------
Project
--------------------------------------------------------------------------
License:   
Copyright 2021 Haruto Sasajima

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGEself.
--------------------------------------------------------------------------
Code Overview:

This code should first connect the client to the server. It should then turn 
off all LED lights initially. Afterwards, it will then prompt the microphone to 
begin continuously collecting input data. Once a certain noise threshold from 
the environment is passed and power is on, the LED strip will turn on all 
white. If this threshold is passed while the LEDs are on, it will turn off all 
of the LEDs. When the LEDs are turned on, the user can press on the buttons to 
change the color settings of the LEDs. The three settings are warm colors, cool 
colors, and rainbow.  The code is formatted so that unless the LEDs are first 
turned on by a clap, it will not turn on even when the buttons are pressed. 
Once it recognizes that a certain button is pressed while the lights are on, 
the color settings corresponding to that button are sent into the LEDs and are 
kept at that setting. The color setting functions are threaded so that the user 
can switch between settings at any time while the LEDs are on. 
"""
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM

import sounddevice as sd
import numpy as np

import time
import opc

power = False

sd.default.device = 0

device_list = sd.query_devices()

print(device_list[0])

ADDRESS = 'localhost:7890'

# Create a client object
client = opc.Client(ADDRESS)

# Test if it can connect
if client.can_connect():
    print ('connected to %s' % ADDRESS)
else:
    # We could exit here, but instead let's just print a warning
    # and then keep trying to send pixels in case the server
    # appears later
    print ('WARNING: could not connect to %s' % ADDRESS)

# Strip contains 240 LEDs
STR_LEN=240
# Turns off LEDs initially
for i in range(STR_LEN):
    leds = [(0, 0, 0)] * STR_LEN

if not client.put_pixels(leds, channel=0):
    print ('not connected')    

# Get input from the microphone
def print_sound(indata, outdata, frames, time):
    volume_norm = np.linalg.norm(indata)*10
    global power
        
# Turns LEDs off if noise level threshold is passed and if LEDs are currently 
# on. Else, it turns them on all white            
    if volume_norm > 20:
        if power: 
            STR_LEN=240
            for i in range(STR_LEN):
                leds = [(0, 0, 0)] * STR_LEN
            
            if not client.put_pixels(leds, channel=0):
                print ('not connected')
            power = False
            sd.sleep(300)
        else:
        # Define Pixel String
            STR_LEN=240
            for i in range(STR_LEN):
                leds = [(255, 255, 255)] * STR_LEN
            
            if not client.put_pixels(leds, channel=0):
                print ('not connected')
            power = True   
            sd.sleep(300)


class ledsetting():
    warm_button     = None
    cold_button     = None
    rain_button     = None
    
    def __init__(self, warm_button="P2_2", cold_button="P2_4", rain_button="P2_6",):
        """ Initialize variables"""
        self.warm_button     = warm_button
        self.cold_button     = cold_button
        self.rain_button     = rain_button
        self._setup()

    # End def
    
    def _setup(self):
        """Setup the hardware components."""
        # Initialize Buttons
        GPIO.setup(self.warm_button, GPIO.IN)
        GPIO.setup(self.cold_button, GPIO.IN)
        GPIO.setup(self.rain_button, GPIO.IN)
        
    # End def

    def warm(self):
        while(1): 
            while(GPIO.input(self.warm_button) == 1): #waiting for press
                time.sleep(0.1)
            if power:
                for i in range(0,STR_LEN,3): #change color array
                    leds[i] = (255, 0, 0)
                    leds[i+1] = (255, 64, 0)
                    leds[i+2] = (255, 128, 0)
                if not client.put_pixels(leds, channel=0): #sends color array over
                    print ('not connected')
            # Wait for button release
            while(GPIO.input(self.warm_button) == 0): 
                # Sleep for a short period of time to reduce CPU load
                time.sleep(0.1)
    # End def
    
    def cold(self):
        while(1): #so the program doesn't stop after one press
            while(GPIO.input(self.cold_button) == 1): #waiting for press
                time.sleep(0.1)
            if power:
                for i in range(0,STR_LEN,3): #change color array
                    leds[i] = (200, 0, 255)
                    leds[i+1] = (0, 0, 255)
                    leds[i+2] = (0, 255, 0)
                if not client.put_pixels(leds, channel=0): #sends color array over
                    print ('not connected')
            # Wait for button release
            while(GPIO.input(self.cold_button) == 0): 
                # Sleep for a short period of time to reduce CPU load
                time.sleep(0.1)
    # End def
    
    def rainbow(self):
        while(1): #so the program doesn't stop after one press
            while(GPIO.input(self.rain_button) == 1): #waiting for press
                time.sleep(0.1)
            if power:
                for i in range(0,STR_LEN,6): #change color array
                    leds[i] = (255, 0, 0)
                    leds[i+1] = (255, 127, 0)
                    leds[i+2] = (255, 255, 0)
                    leds[i+3] = (0, 255, 0)
                    leds[i+4] = (0, 0, 255)
                    leds[i+5] = (75, 0, 130)
                if not client.put_pixels(leds, channel=0): #sends color array over
                    print ('not connected')
            # Wait for button release
            while(GPIO.input(self.rain_button) == 0): 
                # Sleep for a short period of time to reduce CPU load
                time.sleep(0.1)
    # End def
        
if __name__ == '__main__': 
    # prompts microphone to start collecting input data
    with sd.InputStream(channels = 1, callback=print_sound):
        import threading
        
        color_settings = ledsetting()
        # threading allows for buttons to be switched between 
        try:
            thread1 = threading.Thread(target=color_settings.warm)
            thread2 = threading.Thread(target=color_settings.cold)
            thread3 = threading.Thread(target=color_settings.rainbow)
            thread1.start()
            thread2.start()
            thread3.start()
            thread1.join()
            thread2.join()
            thread3.join()
            
        except KeyboardInterrupt:
            pass
    
        print("Program Complete.")        
