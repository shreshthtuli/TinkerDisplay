import ASUS.GPIO as GPIO
import time

GPIO.setmode (GPIO.BOARD)
GPIO.setwarnings(False)

pin1=3
pin2=5
pin3=8
pin4=10
pin5=24
pin6=23
pin7=22
pin8=21

delay = 0.2
counter = 0
limit = 100

matrix  =  [[0, 0, 0, 0],
	    [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]

#For 3.3 static
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, 1)
GPIO.setup(38, GPIO.OUT)
GPIO.output(38, 1)
GPIO.setup(36, GPIO.OUT)
GPIO.output(36, 1)

def setup():
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.setup(pin3, GPIO.OUT)
    GPIO.setup(pin4, GPIO.OUT)
    GPIO.setup(pin5, GPIO.OUT)
    GPIO.setup(pin6, GPIO.OUT)
    GPIO.setup(pin7, GPIO.OUT)
    GPIO.setup(pin8, GPIO.OUT)

def off():
    GPIO.output(pin1, 0)
    GPIO.output(pin2, 0)
    GPIO.output(pin3, 0)
    GPIO.output(pin4, 0)
    GPIO.output(pin5, 0)
    GPIO.output(pin6, 0)
    GPIO.output(pin7, 0)
    GPIO.output(pin8, 0)


def glow(col, r1, r2, r3, r4):
    GPIO.output(24-col, 1)
    GPIO.output(pin1, 1-r1)
    GPIO.output(pin2, 1-r2)
    GPIO.output(pin3, 1-r3)
    GPIO.output(pin4, 1-r4)
    time.sleep(delay)
    off()

def high(a):
    if a < 2:
        return a
    else:
        return 1

def low(a):
    if a < 2:
	return a
    else:
        return 0

def transform(r1, r2, r3, r4):
    global counter
    counter += 1
    if counter > 2*limit:
	counter = 0
    if counter > limit:
	return (low(r1), low(r2), low(r3), low(r4))
    else:
        return (high(r1), high(r2), high(r3), high(r4))
        

def display():
    for col in range(4):
        r1, r2, r3, r4 = transform(matrix[col][0], matrix[col][1], matrix[col][2], matrix[col][3])
        glow(col, r1, r2, r3, r4) 
        time.sleep(delay)


# MAIN CODE

setup()
off()

matrix  =  [[2, 0, 0, 0],
	    [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]

for i in range(100):
    display()

matrix  =  [[2, 0, 0, 0],
	    [0, 2, 0, 0],
            [0, 0, 2, 0],
            [0, 0, 0, 2]]

for i in range(200):
    display()

GPIO.cleanup()
