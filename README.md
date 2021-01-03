# TeslaRadio

This code will be used for a Tesla* Radio project. (* - not related to Elon's Tesla)

## History
I happened to come across few Tesla ARS 236 radios made in Czechoslovakia somewhere around 1970 -1980. It contains a nice all-around speaker and in general is of some old-school cool design.

Tesla ARS 236 in video: https://www.youtube.com/watch?v=bsh7unEFyhs

## The Plan
* build a wooden housing (with respect to the original design)
* put two speakers inside together with RPiZW, HiFiBerry MiniAMP and KY040
* program some knob interface (push_and_turn)

## The HW
* 2x Tesla ARS 236
* Rpi Zero W
* HiFiBerry MiniAMP
* KY040 Rotary Encoder
* Waveshare 1.5 128x128 OLED display

### KY040 wiring
* CLK - PIN 29 (GPIO  5)
* DT  - PIN 31 (GPIO  6)
* SW  - PIN 33 (GPIO 13)
* VCC - 3v3 (any)
* GND - Ground (any)

### OLED wiring
* DIN - PIN 19 (GPIO 10) - SPI0 MOSI
* CLK - PIN 23 (GPIO 11) - SPI0 SCLK
* DC  - PIN 18 (GPIO 24)
* CS  - PIN 24 (GPIO  8) - SPI0 CE0
* RST - PIN 22 (GPIO 25)
* VCC - 3v3 (any)
* GND - Ground (any)

## Final wiring
(shown on test RPi4 in a Nes4Pi case)
![alt text](https://github.com/ntnlabs/TeslaRadio/blob/main/PXL_20210103_020910203.NIGHT.jpg)

## The SW
* python3.7
* pyky040 module
* luma.oled drivers
* mpd & mpc for media player
* some ttf fonts

## Features (please note, some of those may be still in progress)
* online radio play
* mp3 (local storage) play
* bluetooth play
* display

# Warnings
I'm using [my fork](https://github.com/ntnlabs/pyKY040/blob/master/pyky040/pyky040.py) of pyky040 library. These are my changes:
* long/short push detection
