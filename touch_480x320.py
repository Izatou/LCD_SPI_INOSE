
from PIL import Image
import RPi.GPIO
import sys
import time
import Python_ILI9486 as TFT
sys.path.append("../../")
from gfxlcd.driver.ili9486.spi import SPI
from gfxlcd.driver.ili9486.ili9486 import ILI9486
RPi.GPIO.setmode(RPi.GPIO.BCM)


disp = TFT.ILI9486(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
disp.begin()


desktop = Image.open('/home/pi/LCD_SPI_INOSE/awal.png')
desktop = desktop.rotate(180).resize((320,480))
lcd_tft = ILI9486(320, 480, SPI())
lcd_tft.rotation = 180

lcd_tft.init()

disp.display(screen_2)


#numbers_image = Image.open("assets/dsp2017_101_64.png")
#lcd_tft.transparency_color = (0, 0, 0)
#lcd_tft.draw_image(10, 10, numbers_image)

def callback(position):
    print('(x,y)', position)

touch = XPT2046(480, 320, 17, callback, 7)
#touch.rotate = 270

touch.init()

while True:
    try:
        time.sleep(1)

    except KeyboardInterrupt:
        touch.close()
        # RPi.GPIO.cleanup()
