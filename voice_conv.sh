#!/bin/sh
arecord -D plughw:0,0 test.wav -d 5 -r 16000
flac test.wav -f --best --sample-rate 16000 -s -o voice.flac

exit 0
