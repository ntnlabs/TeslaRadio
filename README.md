# TeslaRadio

This code will be used for a Tesla* Radio project. (* - not related to Elon's Tesla)

## History
I happened to come across few Tesla ARS 236 radios made in Czechoslovakia somewhere around 1970 -1980. It contains a nice all-around speaker and in general is of some old-school cool design.

Tesla ARS 236 in video: https://www.youtube.com/watch?v=bsh7unEFyhs

## The Plan
* build a wooden housing (with respect to the original design)
* put two speakers inside together with RPiZW, HiFiBerry MiniAMP and KY040
* program some knob interface (push_and_turn)

## Features (please note, some of those may be still in progress)
* online radio play
* mp3 (local storage) play
* bluetooth play
* display

# Warnings
I'm using my fork of pyky040 library. These are my changes:
* long/short push detection
