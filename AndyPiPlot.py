#!usr/bin/python
#
# Python Script:	Pygame based graph class for AndyPi TFT screens
# Author:			AndyPi 
# Date:				24/02/2015
# Version:			1.0
#
# This python class can be called from your python code
# Please see the usetest file for samples and instructions.
#
# import numpy as np
# from time import strftime
# 
# TODO: blit to screen test

import matplotlib
import pygame
from pygame.locals import *

# Force matplotlib to not use any Xwindows backend.
matplotlib.use("Agg")
from matplotlib import pyplot

# Set the display to fb1 - i.e. the TFT
os.environ["SDL_FBDEV"] = "/dev/fb1"
# Remove mouse
os.environ["SDL_NOMOUSE"]="1"

# initialise pygame module
pygame.init()

# set up the window
screen = pygame.display.set_mode((320, 240), 0, 32)

# setup lists
x=[]
y=[]

class AndyPiPlot():

    def readData(self,fileName):
	    readFile = open(fileName, 'r') # open the file
        sepFile = readFile.read().split('\n')
        readFile.close()

        for plotPair in sepFile:
            xAndY = plotPair.split(',')
            x.append(int(xAndY[0]))
            y.append(int(xAndY[1]))

	return (x,y)
    
	# scatter plot
    def scatterPlot(self,outputFile,varTitle,varXlabel,varYlabel,x,y): 
		fig=pyplot.figure()
		rect = fig.patch
		rect.set_facecolor('black')	
		ax1=fig.add_subplot(1,1,1, axisbg='black') #1,1,1, = 1x1 chart, select plot 1 of 1
		ax1.tick_params(axis='x', colors='white')
		ax1.tick_params(axis='y', colors='white')
		ax1.spines['bottom'].set_color('white')
		ax1.spines['top'].set_color('white')
		ax1.spines['left'].set_color('white')
		ax1.spines['right'].set_color('white')
        ax1.set_title(varTitle, color='white')
        ax1.set_xlabel(varXlabel, color='white')
        ax1.set_ylabel(varYlabel, color='white')

        plt.scatter(x, y, alpha=0.5)
        pyplot.savefig(outputFile, facecolor=fig.get_facecolor() ,bbox_inches='tight', dpi=80,pad_inches=0.03)
		blitimage(outputFile)


	# plots one line on one one set of axes
    def linePlot1(self,outputFile,varTitle,varXlabel,varYlabel,x,y):  
		fig=pyplot.figure()
		rect = fig.patch
		rect.set_facecolor('black')	
		ax1=fig.add_subplot(1,1,1, axisbg='black') #1,1,1, = 1x1 chart, select plot 1 of 1
		ax1.tick_params(axis='x', colors='white')
		ax1.tick_params(axis='y', colors='white')
		ax1.spines['bottom'].set_color('white')
		ax1.spines['top'].set_color('white')
		ax1.spines['left'].set_color('white')
		ax1.spines['right'].set_color('white')
        ax1.set_title(varTitle, color='white')
        ax1.set_xlabel(varXlabel, color='white')
        ax1.set_ylabel(varYlabel, color='white')
		ax1.plot(x,y,'white', linewidth=2)
        pyplot.savefig(outputFile, facecolor=fig.get_facecolor() ,bbox_inches='tight', dpi=80,pad_inches=0.03)
		blitimage(outputFile)
	
	# plots two lines on the same set of axes
    def linePlot2(self,outputFile,varTitle,varXlabel,varYlabel,x1,y1,varDataset1,data1Color,x2,y2,varDataset2,data2Color): 
		fig=pyplot.figure()
		rect = fig.patch
		rect.set_facecolor('black')
		ax1=fig.add_subplot(1,1,1, axisbg='black') #1,1,1, = 1x1 chart, select plot 1 of 1
		ax1.tick_params(axis='x', colors='white')
		ax1.tick_params(axis='y', colors='white')
		ax1.spines['bottom'].set_color('white')
		ax1.spines['top'].set_color('white')
		ax1.spines['left'].set_color('white')
		ax1.spines['right'].set_color('white')
		ax1.plot(x1,y1,data1Color,label=varDataset1)
		ax1.plot(x2,y2,data2Color,label=varDataset2)
		ax1.legend(loc="best")
		#	ax1.legend.frame.set_facecolor('black')
		#	ax1.legend.frame.set_edgecolor('white')
        ax1.set_title(varTitle, color='white')
        ax1.set_xlabel(varXlabel, color='white')
        ax1.set_ylabel(varYlabel, color='white')
        pyplot.savefig(outputFile, facecolor=fig.get_facecolor() ,bbox_inches='tight', dpi=80,pad_inches=0.03)
		blitimage(outputFile)

	def blitimage(self, outputFile): # need to test this section
		image = pygame.image.load(outputFile)
		screen.blit(image, (0, 0))
		pygame.display.flip()
		pygame.display.update()
		
    def main(self):
	# enter some sample data to plot
		x1=[1,3,5,7,9,11]
		y1=[5,10,15,30,90,93]
		x2=[1,3,5,7,9,11]
		y2=[11,32,54,76,99,101]
		self.linePlot2("test.png","AndyPi is amazing","X label","Y label",x1,y1,'Super 1',"yellow",x2,y2,'Super 2',"red");

if __name__ == '__main__':
    plotter=AndyPiPlot()
    plotter.main()
