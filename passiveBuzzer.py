#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import sys
from random import randint
import zmq

Buzzer = 11

CL = [0, 131, 147, 165, 175, 196, 211, 248]         # Frequency of Low C notes

CM = [0, 262, 294, 330, 350, 393, 441, 495]         # Frequency of Middle C notes

CH = [0, 525, 589, 661, 700, 786, 882, 990]         # Frequency of High C notes

song_1 = [  CM[3], CM[5], CM[6], CM[3], CM[2], CM[3], CM[5], CM[6], # Notes of song1
            CH[1], CM[6], CM[5], CM[1], CM[3], CM[2], CM[2], CM[3],
            CM[5], CM[2], CM[3], CM[3], CL[6], CL[6], CL[6], CM[1],
            CM[2], CM[3], CM[2], CL[7], CL[6], CM[1], CL[5] ]

beat_1 = [  1, 1, 3, 1, 1, 3, 1, 1,                         # Beats of song 1, 1 means 1/8 beats
            1, 1, 1, 1, 1, 1, 3, 1,
            1, 3, 1, 1, 1, 1, 1, 1,
            1, 2, 1, 1, 1, 1, 1, 1,
            1, 1, 3 ]

song_2 = [  CM[1], CM[1], CM[1], CL[5], CM[3], CM[3], CM[3], CM[1], # Notes of song2
            CM[1], CM[3], CM[5], CM[5], CM[4], CM[3], CM[2], CM[2],
            CM[3], CM[4], CM[4], CM[3], CM[2], CM[3], CM[1], CM[1],
            CM[3], CM[2], CL[5], CL[7], CM[2], CM[1]        ]

beat_2 = [  1, 1, 2, 2, 1, 1, 2, 2,                         # Beats of song 2, 1 means 1/8 beats
            1, 1, 2, 2, 1, 1, 3, 1,
            1, 2, 2, 1, 1, 2, 2, 1,
            1, 2, 2, 1, 1, 3 ]

def setup():
    GPIO.setmode(GPIO.BOARD)                # Numbers GPIOs by physical location
    GPIO.setup(Buzzer, GPIO.OUT)    # Set pins' mode is output
    global Buzz                                             # Assign a global variable to replace GPIO.PWM
    Buzz = GPIO.PWM(Buzzer, 440)    # 440 is initial frequency.                                  # Start Buzzer pin with 50% duty ration

def loop():
    while True:
        #    Playing song 1...
        topic, data = subscriber.recv_multipart()
        stringa_unicode = data.decode('utf-8')
        if(stringa_unicode == "ON"):
            Buzz.start(50)
            i=1
            while( stringa_unicode == "ON" and i<len(song_1)):
                topic, data = subscriber.recv_multipart()
                stringa_unicode = data.decode('utf-8')
                Buzz.ChangeFrequency(song_1[i]) # Change the frequency along the song note
                time.sleep(beat_1[i] * 0.5)             # delay a note for beat * 0.5s
                i+=1
            Buzz.stop()

def destory():
    Buzz.stop()                                     # Stop the buzzer
    GPIO.output(Buzzer, 1)          # Set Buzzer pin to High
    GPIO.cleanup()                          # Release resource

if __name__ == '__main__':          # Program start from here
    setup()
    ctx = zmq.Context.instance()
    subscriber = ctx.socket(zmq.SUB)
    url = "tcp://localhost:5560"
    subscriber.connect(url)

    subscription = b"PASSIVEBUZZER"
    subscriber.setsockopt(zmq.SUBSCRIBE, subscription)
    try:
        loop()
    except KeyboardInterrupt:       # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destory()
