#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  viewer.py
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

import pygtk
import gtk
import glob

class Plot_Viewer:
	dragging = False
	curframe = 0
	lastx = 0
	
	dragging2 = False
	curframe2 = 0
	lastx2 = 0
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("motion_notify_event", self.mouse_move)
		self.window.connect("button_press_event", self.button_press)
		self.window.connect("button_release_event", self.button_release)
		self.window.connect("destroy", self.destroy)
		self.window.set_events(gtk.gdk.BUTTON_PRESS_MASK|gtk.gdk.BUTTON_RELEASE_MASK|gtk.gdk.POINTER_MOTION_MASK)
		
		self.images = []
		files = glob.glob('rgbplotframe*')
		files.sort()
		for i in files:
			frame = gtk.Image()
			frame.set_from_file(i)
			frame.show()
			self.images.extend([frame])
			
		self.window.add(self.images[0])
		self.window.show()
		
		self.window2 = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window2.connect("motion_notify_event", self.mouse_move2)
		self.window2.connect("button_press_event", self.button_press2)
		self.window2.connect("button_release_event", self.button_release2)
		self.window2.connect("destroy", self.destroy)
		self.window2.set_events(gtk.gdk.BUTTON_PRESS_MASK|gtk.gdk.BUTTON_RELEASE_MASK|gtk.gdk.POINTER_MOTION_MASK)
		
		self.images2 = []
		files = glob.glob('hsvplotframe*')
		files.sort()
		for i in files:
			frame = gtk.Image()
			frame.set_from_file(i)
			frame.show()
			self.images2.extend([frame])
			
		self.window2.add(self.images2[0])
		self.window2.show()
	
	def main(self):
		gtk.main()
		
	def destroy(self, data=None):
		gtk.mainquit()
		
	def mouse_move(self, widget, event, data=None):
		if self.dragging:
			self.window.remove(self.images[int(self.curframe)])
			self.curframe = (self.curframe + (self.lastx - event.x)/15)%len(self.images)
			self.window.add(self.images[int(self.curframe)])
			self.lastx = event.x

	def button_press(self, widget, event, data=None):
		if event.button == 1:
			self.lastx = event.x
			self.dragging = True

	def button_release(self, widget, event, data=None):
		self.dragging = False
		
	def mouse_move2(self, widget, event, data=None):
		if self.dragging2:
			self.window2.remove(self.images2[int(self.curframe2)])
			self.curframe2 = (self.curframe2 + (self.lastx2 - event.x)/15)%len(self.images2)
			self.window2.add(self.images2[int(self.curframe2)])
			self.lastx2 = event.x

	def button_press2(self, widget, event, data=None):
		if event.button == 1:
			self.lastx2 = event.x
			self.dragging2 = True

	def button_release2(self, widget, event, data=None):
		self.dragging2 = False
def main():
	
	return 0

if __name__ == '__main__':
	prg = Plot_Viewer()
	prg.main()

