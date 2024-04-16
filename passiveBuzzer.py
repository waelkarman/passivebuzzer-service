#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import sys
from random import randint
import zmq

Buzzer = 11

def setup():
    GPIO.setmode(GPIO.BOARD)                # Numbers GPIOs by physical location
    GPIO.setup(Buzzer, GPIO.OUT)    # Set pins' mode is output
    global Buzz                                             # Assign a global variable to replace GPIO.PWM
    Buzz = GPIO.PWM(Buzzer, 440)    # 440 is initial frequency.                                  # Start Buzzer pin with 50% duty ration

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
    stringa_unicode = "Buzzer OFF"
    
    while(True):
        topic, data = subscriber.recv_multipart()
        stringa_unicode = data.decode('utf-8')
        if(stringa_unicode == "Buzzer ON"):    
            Buzz.start(50)
        else:
            Buzz.stop()

    destory()
