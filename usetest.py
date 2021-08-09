#!usr/bin/python
#
# Python Script:	Pygame based graph class for AndyPi TFT screens
# Author: 			AndyPi 
# Date:				24/02/2015
# Version:			1.0
#
# **** INSTRUCTIONS ****
# 
# Software requirements:
# 	install python & setuptools
# 	install python-matplotlib
# 	install python-scipy
#	AndyPiPlot.py (python class)
#
# Functions:
#	
#		a: Read data from csv file helper function
#			var1, var2 = readData("yourdata.csv")
#	
# 		1: Single line plot 
#			plt.linePlot1(outputFile, Title text, X label text , Y label text, x variable ,y variable)
#			
#		2: Dual plot with legend
#			plt.linePlot2(outputFile, Title text, X label text , Y label text, __
#			__x variable data set 1, y variable data set 1, data set 1 label, data set 1 colour__
#			__x variable data set 2, y variable data set 2, data set 2 label, data set 2 colour)
#
#		3: Scatter plot
#			plt.scatterPlot(outputFile, Title text, X label text , Y label text, x variable ,y variable)
#
#		4: Bar plot
#			TODO

# import AndyPiPlot class
from AndyPiPlot import *

# set object name
plt=AndyPiPlot()

# Read in the data from 2 CSV files and assign to variables
x1, y1 = plt.readData("sample.csv")
x2, y2 = plt.readData("sample2.csv")

# call the linePlot2 function using your data and options
# this plots the data as a file, and then blits it onto the AndyPi TFT
plt.linePlot2("tft.png","Andy is amazing (and clearly narcissistic)","Time","Money",x1,y1,"Andy Pi Sales","green",x2,y2,"Andy's Kudos","red");

