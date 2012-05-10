#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
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

import sys
import cv

dragging = False
tubex = 0
tubey = 0
tubew = 0
tubeh = 0

def mouse_drag(event, x, y, flags, params):
	changed = False
	if event == cv.CV_EVENT_LBUTTONDOWN:
		dragging = True
		tubex = x
		tubey = y
		changed = True
	elif event == cv.CV_EVENT_MOUSEMOVE and dragging == True:
		tubew = x - tubex
		tubeh = y - tubey
		changed = True
	elif event == cv.CV_EVENT_LBUTTONUP:
		dragging = False
		tubew = x - tubex
		tubeh = y - tubeh
		changed = True
	if changed:
		

def hs_histogram(src):
	hsv = cv.CreateImage(cv.GetSize(src), 8, 3)
	cv.CvtColor(src, hsv, cv.CV_BGR2HSV)
	
	h_plane = cv.CreateMat(src.rows, src.cols, cv.CV_8UC1)
	s_plane = cv.CreateMat(src.rows, src.cols, cv.CV_8UC1)
	cv.Split(hsv, h_plane, s_plane, None, None)
	planes = [h_plane, s_plane]
	
	h_bins = 30
	s_bins = 32
	hist_size = [h_bins, s_bins]
	h_ranges = [0, 180]
	s_ranges = [0, 255]
	ranges = [h_ranges, s_ranges]
	scale = 10
	
	hist = cv.CreateHist([h_bins, s_bins], cv.CV_HIST_ARRAY, ranges, 1)
	cv.CalcHist([cv.GetImage(i) for i in planes], hist)
	(_, max_value, _, _) = cv.GetMinMaxHistValue(hist)
	
	hist_img = cv.CreateImage((h_bins*scale, s_bins*scale), 8, 3)
	
	for h in range(h_bins):
		for s in range(s_bins):
			bin_val = cv.QueryHistValue_2D(hist, h, s)
			intensity = cv.Round(bin_val*255/max_value)
			cv.Rectangle(hist_img,
						 (h*scale, s*scale),
						 ((h+1)*scale - 1, (s+1)*scale - 1),
						 cv.RGB(intensity, intensity, intensity),
						 cv.CV_FILLED)
	return hist_img

def main():
	src = cv.LoadImageM(sys.argv[1])
	display = cv.CreateMat(
	
	cv.NamedWindow("Source", 1)
	cv.ShowImage("Source", src)
	dragging = false
	cv.SetMouseCallback("Source", mouse_drag, (src))
	
	cv.NamedWindow("Tubes", 1)
	cv.WaitKey(0)
	
	return 0

if __name__ == '__main__':
	main()

