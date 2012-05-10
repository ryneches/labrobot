#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  segmenttest.py
#  
#  Copyright 2012 Keegan Owsley <keegan@keegan-desktop>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import cv
import sys
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import pylab
import scipy

mode = 'rgb'

def coloredpixels(image, color):
	for row in range(image.height-1):
		for col in range(image.width-1):
			if image[row+1,col+1] == color:
				yield (row,col)
				
class segmentProg:
	smallsize = (1024, 768)
	window_name = 'Image'
	drawing = False
	brushcolor = (0, 0, 255)
	brushlocation = (0, 0)
	brushthickness = 10
	def __init__(self, image_filename):
		self.image = cv.LoadImage(image_filename, cv.CV_LOAD_IMAGE_COLOR)
		
		self.depth = self.image.depth
		self.smallimg = cv.CreateImage(self.smallsize, self.depth, 
										self.image.channels)
		self.mask = cv.CreateImage(self.smallsize, self.depth, 3)
		
		self.canvas = cv.CreateImage(self.smallsize, self.depth, 3)
		
		cv.Resize(self.image, self.smallimg)
	
		self.image = cv.LoadImage(image_filename, cv.CV_LOAD_IMAGE_COLOR)
		self.gray = cv.CreateImage(self.smallsize, self.depth, 1)
		self.hsv = cv.CreateImage(self.smallsize, self.depth, 3)
		self.hue = cv.CreateImage(self.smallsize, self.depth, 1)
		self.sat = cv.CreateImage(self.smallsize, self.depth, 1)
		self.val = cv.CreateImage(self.smallsize, self.depth, 1)
		
		cv.CvtColor(self.smallimg,self.hsv,cv.CV_BGR2HSV)
	
		cv.Split(self.hsv, self.hue, self.sat, self.val, None)
	
		self.out = cv.CreateImage(self.smallsize, self.depth, 1)
		
		self.histfig = plt.figure()
		self.figure = plt.figure()
		self.histax = self.histfig.add_subplot(111)
		self.axes = self.figure.add_subplot(111, projection='3d')
		if mode == 'hsv':
			self.axes.set_xlabel('Hue')
			self.axes.set_ylabel('Saturation')
			self.axes.set_zlabel('Value')
		else:
			self.axes.set_xlabel('Blue')
			self.axes.set_ylabel('Green')
			self.axes.set_zlabel('Red')
		plt.draw()
		#self.axes.mouse_init()
	
	def main(self):
		self.window = cv.NamedWindow(self.window_name, cv.CV_WINDOW_AUTOSIZE)
		cv.SetMouseCallback(self.window_name, self.mouse_callback, None)
		cv.ShowImage(self.window_name, self.smallimg)
		cv.WaitKey()
		print 'Writing animations...'
		self.axes.mouse_init()
		
		global mode
		
		mode = 'rgb'
		self.draw_huge_plot()
		#Generate animation
		for i in range(50):
			fname = 'rgbplotframe%03d.png'%i
			self.axes.view_init(azim=360/50*i)
			self.figure.savefig(fname)
		
		mode = 'hsv'
		self.draw_huge_plot()
		#Generate animation
		for i in range(50):
			fname = 'hsvplotframe%03d.png'%i
			self.axes.view_init(azim=360/50*i)
			self.figure.savefig(fname)
			
			
	def mouse_callback(self, event, x, y, flags, param):
		if event == cv.CV_EVENT_MOUSEMOVE and self.drawing == True:
			cv.Line(self.mask, self.brushlocation, (x,y), 
					self.brushcolor, self.brushthickness)
			self.update(list(self.brushlocation), [x,y])
			self.brushlocation = (x,y)
		elif event == cv.CV_EVENT_LBUTTONDOWN:
			self.drawing = True
			self.brushlocation = (x,y)
			self.brushcolor = (0, 255, 0)
		elif event == cv.CV_EVENT_RBUTTONDOWN:
			self.drawing = True
			self.brushlocation = (x,y)
			self.brushcolor = (0, 0, 255)
		elif event == cv.CV_EVENT_RBUTTONUP or event == cv.CV_EVENT_LBUTTONUP:
			self.drawing = False
			self.draw_plot()
			
	def update(self, loc1, loc2):
		if loc1[0] > loc2[0]:
			temp = loc2[0]
			loc2[0] = loc1[0]
			loc1[0] = temp
		if loc1[1] > loc2[1]:
			temp = loc2[1]
			loc2[1] = loc1[1]
			loc1[1] = temp
		cv.Add(self.smallimg, self.mask, self.canvas)
		cv.ShowImage(self.window_name, self.canvas)
		
	
	def draw_plot(self):
		self.axes.clear()
		self.histax.clear()
		global mode
		if mode == 'hsv':
			self.axes.set_xlabel('Hue')
			self.axes.set_ylabel('Saturation')
			self.axes.set_zlabel('Value')
			tubepixels = np.array(list(self.hsv[greenloc[0], greenloc[1]] for greenloc in coloredpixels(self.mask, (0,255,0))))
			nontubepixels = np.array(list(self.hsv[redloc[0], redloc[1]] for redloc in coloredpixels(self.mask, (0,0,255))))
		else:
			self.axes.set_xlabel('Blue')
			self.axes.set_ylabel('Green')
			self.axes.set_zlabel('Red')
			tubepixels = np.array(list(self.smallimg[greenloc[0], greenloc[1]] for greenloc in coloredpixels(self.mask, (0,255,0))))
			nontubepixels = np.array(list(self.smallimg[redloc[0], redloc[1]] for redloc in coloredpixels(self.mask, (0,0,255))))
		onehundredtube = [int(x) for x in scipy.linspace(0,len(tubepixels)-1, 500)]
		onehundrednon = [int(x) for x in scipy.linspace(0,len(nontubepixels)-1, 500)]
		if len(tubepixels):
			self.axes.scatter(tubepixels[onehundredtube,0], tubepixels[onehundredtube,1], tubepixels[onehundredtube,2], c='g')
			self.histax.hist(tubepixels[onehundredtube, 1], 100, normed=1, facecolor='green')
		if len(nontubepixels):
			self.axes.scatter(nontubepixels[onehundrednon,0], nontubepixels[onehundrednon,1], nontubepixels[onehundrednon,2], c='r')
			self.histax.hist(nontubepixels[onehundrednon, 1], 100, normed=1, facecolor='red')
		self.figure.canvas.draw()
		self.histfig.canvas.draw()
		
	def draw_huge_plot(self):
		global mode
		self.axes.clear()
		if mode == 'hsv':
			self.axes.set_xlabel('Hue')
			self.axes.set_ylabel('Saturation')
			self.axes.set_zlabel('Value')
			tubepixels = np.array(list(self.hsv[greenloc[0], greenloc[1]] for greenloc in coloredpixels(self.mask, (0,255,0))))
			nontubepixels = np.array(list(self.hsv[redloc[0], redloc[1]] for redloc in coloredpixels(self.mask, (0,0,255))))
		else:
			self.axes.set_xlabel('Blue')
			self.axes.set_ylabel('Green')
			self.axes.set_zlabel('Red')
			tubepixels = np.array(list(self.smallimg[greenloc[0], greenloc[1]] for greenloc in coloredpixels(self.mask, (0,255,0))))
			nontubepixels = np.array(list(self.smallimg[redloc[0], redloc[1]] for redloc in coloredpixels(self.mask, (0,0,255))))
		onehundredtube = [int(x) for x in scipy.linspace(0,len(tubepixels)-1, 10000)]
		onehundrednon = [int(x) for x in scipy.linspace(0,len(nontubepixels)-1, 10000)]
		if len(tubepixels):
			self.axes.scatter(tubepixels[onehundredtube,0], tubepixels[onehundredtube,1], tubepixels[onehundredtube,2], c='g')
		if len(nontubepixels):
			self.axes.scatter(nontubepixels[onehundrednon,0], nontubepixels[onehundrednon,1], nontubepixels[onehundrednon,2], c='r')
		#plt.draw()

if __name__ == '__main__':
	pylab.ion()
	program = segmentProg(sys.argv[1])
	program.main()
