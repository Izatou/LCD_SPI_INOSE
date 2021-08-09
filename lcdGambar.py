from PIL import Image, ImageDraw, ImageFont

import Python_ILI9486 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import time


# Raspberry Pi configuration.
DC = 24
RST = 25
SPI_PORT = 0
SPI_DEVICE = 0

disp = TFT.ILI9486(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
disp.begin()

disp.clear((255,0,0))

image = Image.open('inosek.png')
image = image.rotate(180).resize((320,480))

draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, 320, 120), fill=(255,138,51))
draw.line((160, 0, 160, 120), fill=(255,255,255))
draw.line((159, 0, 159, 120), fill=(255,255,255))
# Load default font.
font = ImageFont.load_default()

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
draw_rotated_text(image, 'SETTING', (240, 32), 270, font, fill=(255,255,255))
draw_rotated_text(image, ' MULAI ', (80, 32), 270, font, fill=(255,255,255))

# Write buffer to display hardware, must be called to make things visible on the
# display!
#disp.display(image)
disp.display(image)