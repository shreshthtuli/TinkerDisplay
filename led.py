import ASUS.GPIO as GPIO
import time, os, errno

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

delay = 0.002
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

def parse(string):
    string = string.strip()
    if string == '1':
        return (0,0)
    elif string == '2':
	return (0,1)
    elif string == '3':
	return (0,2)
    elif string == 'a':
	return (0,3)
    elif string == '4':
	return (1,0)
    elif string == '5':
	return (1,1)
    elif string == '6':
	return (1,2)
    elif string == 'b':
	return (1,3)
    elif string == '7':
	return (2,0)
    elif string == '8':
	return (2,1)
    elif string == '9':
	return (2,2)
    elif string == 'c':
	return (2,3)
    elif string == '*':
	return (3,0)
    elif string == '0':
	return (3,1)
    elif string == '#':
	return (3,2)
    elif string == 'd':
	return (3,3)
    else:
	return (-1,-1)
   

# MAIN CODE

setup()
off()

FIFO = 'mypipe'

try:
     os.mkfifo(FIFO)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

matrix  =  [[0, 0, 0, 0],
	    [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]

for i in range(1):
    display()


print("Opening FIFO...")
with open(FIFO) as fifo:
    print("FIFO opened")
    while True:
	for i in range(10):
	    display()
	data = fifo.readline()
	if data is None:
	    continue
	print data,
	a,b = parse(data)
	if a == -1 and b == -1:
	    continue
	matrix[a][b] = (matrix[a][b] + 1)%3
	print matrix

GPIO.cleanup()
