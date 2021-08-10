from PIL import Image, ImageDraw, ImageFont
import Python_ILI9486 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import time
from gfxlcd.driver.xpt2046.xpt2046 import XPT2046


# Raspberry Pi configuration.
DC = 24
RST = 25
SPI_PORT = 0
SPI_DEVICE = 0

disp = TFT.ILI9486(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
disp.begin()
#disp.clear((255,0,0))

desktop = Image.open('/home/pi/LCD_SPI_INOSE/awal.png')
desktop = desktop.rotate(180).resize((320,480))

image = Image.open('/home/pi/LCD_SPI_INOSE/inosek.png')
image = image.rotate(180).resize((320,480))

screen_2 = Image.open('/home/pi/LCD_SPI_INOSE/MOCKUP_INOSE/2.png')
screen_2 = screen_2.rotate(180).resize((320,480))

screen_3 = Image.open('/home/pi/LCD_SPI_INOSE/MOCKUP_INOSE/3.png')
screen_3 = screen_3.rotate(180).resize((320,480))

screen_4 = Image.open('/home/pi/LCD_SPI_INOSE/MOCKUP_INOSE/4.png')
screen_4 = screen_4.rotate(180).resize((320,480))

screen_5 = Image.open('/home/pi/LCD_SPI_INOSE/MOCKUP_INOSE/5.png')
screen_5 = screen_5.rotate(180).resize((320,480))

screen_6 = Image.open('/home/pi/LCD_SPI_INOSE/MOCKUP_INOSE/6.png')
screen_6 = screen_6.rotate(180).resize((320,480))

draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, 320, 120), fill=(255,138,51))
draw.line((160, 0, 160, 120), fill=(255,255,255))
draw.line((159, 0, 159, 120), fill=(255,255,255))
# Load default font.
fontEn = ImageFont.truetype('/home/pi/LCD_SPI_INOSE/miniN.ttf', 75)

def draw_rotated_text(image, text, position, angle, font, fill=(255,255,255)):
	# Get rendered font width and height.
	draw = ImageDraw.Draw(image)
	width, height = draw.textsize(text, font=font)
	# Create a new image with transparent background to store the text.
	textimage = Image.new('RGBA', (width, height), (0,0,0,0))
	# Render the text.
	textdraw = ImageDraw.Draw(textimage)
	textdraw.text((0,0), text, font=font, fill=fill)
	# Rotate the text image.
	rotated = textimage.rotate(angle, expand=1)
	# Paste the text into the image, using it as a mask for transparency.
	image.paste(rotated, position, rotated)

# Write two lines of white text on the buffer, rotated 90 degrees counter clockwise.
draw_rotated_text(screen_3, '97%', (140, 230), 270, fontEn, fill=(255,138,51))
draw_rotated_text(screen_5, '89%', (170, 250), 270, fontEn, fill=(255,138,51))
draw_rotated_text(screen_5, 'Positif', (100, 200), 270, fontEn, fill=(255,138,51))
page=0
# Write buffer to display hardware, must be called to make things visible on the
# display!
#disp.display(image)

def callback(position):
    #print('(x,y)', position)
	if position[0] > 350:
		if position[1] < 150:
			page=4
	if position[0] > 350:
		if position[1] > 150:
			page=3
	

touch = XPT2046(480, 320, 17, callback, 7)
#touch.rotate = 270
disp.display(desktop)
time.sleep(3)
disp.display(screen_2)
touch.init()


while True:
    try:
	if page == 0:
		disp.display(screen_2)
	if page == 3:
		disp.display(screen_3)
	if page == 4:
		disp.display(screen_4) 

    except KeyboardInterrupt:
        #touch.close()
        time.sleep(1)
        # RPi.GPIO.cleanup()

# while (1):
	# disp.display(desktop)
	# time.sleep(3)
	#disp.display(image)
	#time.sleep(3)
	# disp.display(screen_2)
	# time.sleep(3)
	# disp.display(screen_3)
	# time.sleep(4)
	# disp.display(screen_4)
	# time.sleep(4)
	# disp.display(screen_5)
	# time.sleep(4)
	# disp.display(screen_2)
	# time.sleep(3)
	# disp.display(screen_6)
	# time.sleep(6)
	# break
#page=0
