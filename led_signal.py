import RPi.GPIO as g
import time
g.setwarnings(False)
g.setmode(g.BCM)

red = 14
yel = 15
green = 18

g.setup(red,g.OUT)
g.setup(yel,g.OUT)
g.setup(green,g.OUT)


def reset_pin():
	g.output(red,g.LOW)
	g.output(yel,g.LOW)
	g.output(green,g.LOW)


def turn_red():
	reset_pin()
	g.output(yel,g.HIGH)
	time.sleep(1)
	reset_pin()
	g.output(red,g.HIGH)

def turn_green():
	reset_pin()
	g.output(green,g.HIGH)

	
