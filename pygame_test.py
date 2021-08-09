#!usr/bin/python
#
# Python Script: Pygame test for AndyPi 2.2" TFT - needs display size editing for 1.8"
# Author: AndyPi 
# Date: 12/09/2014

import pygame, sys, os, math
from pygame.locals import *

# Set the display to fb1 - i.e. the TFT
os.environ["SDL_FBDEV"] = "/dev/fb1"
# Remove mouse
os.environ["SDL_NOMOUSE"]="1"

# Set constants
FPS=30
DISPLAY_H=240 # 120 for 1.8"
DISPLAY_W=320 # 168 for 1.8"
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
IRED  = (176,  23,  21)

# main game loop
def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF=pygame.display.set_mode((DISPLAY_W, DISPLAY_H))

    while True:
        for event in pygame.event.get():
            if event.type ==  QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
  
        doSomething()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


# a funtion to do something
def doSomething():
    DISPLAYSURF.fill(WHITE)
#    pygame.draw.circle(DISPLAYSURF, RED, (100,80), 24, 2)
#    pygame.draw.line(DISPLAYSURF,RED, (160,160), (160,200), 2)
    pygame.draw.arc(DISPLAYSURF, RED, ((120, 50), (80,80)), math.pi/4, math.pi, 10)
    pygame.draw.arc(DISPLAYSURF, IRED, ((120, 60), (80,80)), math.pi/4, math.pi, 10)
    pygame.draw.arc(DISPLAYSURF, RED, ((120, 70), (80,80)), math.pi/4, math.pi, 10)

    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    textSurfaceObj = fontObj.render('AndyPi', True, BLACK, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (160,120)

    DISPLAYSURF.blit (textSurfaceObj, textRectObj)

# Run Main Function
if __name__ == '__main__':
    main()
