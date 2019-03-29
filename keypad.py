import ASUS.GPIO as GPIO
import time

GPIO.setmode (GPIO.BOARD)
GPIO.setwarnings(False)

MATRIX = [ [1,2,3,'a'],
           [4,5,6,'b'],
           [7,8,9,'c'],
           ['*',0,'#','d']]

ROW =   [31,32,33,35]
COL = [11,12,13,15]

for j in range(4):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 1)

for i in range (4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

newkey = ''
oldkey = ''
mypipe = open('mypipe', 'w')
mypipe.write('')
mypipe.close()


try:
    while(True):
    	newkey = ''
        for j in range (4):
            GPIO.output(COL[j],0)
            time.sleep(0.01)

            for i in range(4):
               if GPIO.input (ROW[i]):
                    newkey = MATRIX[i][j]
                    break

            GPIO.output(COL[j],1)
	    time.sleep(0.01)

        if (newkey == '' and oldkey != ''):
        	mypipe = open('mypipe', 'a')
                print oldkey
		mypipe.write(str(oldkey) + "\n")
		mypipe.close()

        oldkey = newkey

except KeyboardInterrupt:
    GPIO.cleanup()
