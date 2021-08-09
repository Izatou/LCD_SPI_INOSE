#from PIL import Image, ImageDraw, ImageFont
from XPT2046 import XPT2046
from sys import stdout

try:
	xpt2046 = XPT2046()
	while True:
		x = xpt2046.readX()
		y = xpt2046.readY()
		z1 = xpt2046.readZ1()
		z2 = xpt2046.readZ2()
#		pressure = round(xpt2046.readTouchPressure(),2)
		if x in range(200,1850) :
			if y in range(200,1050) :
				#disp.display()
				stdout.write ("X = %s " %x + "Y = %s \n" %y)
				stdout.flush ()
except KeyboardInterrupt:
	stdout.write ("\n")
except Exception:
	raise
