#!/usr/bin/python
# -*- coding: utf-8 -*-

from GUI.MainFrame import *
import os

os.chdir(os.path.dirname(os.path.realpath(__file__))) 	#	This will prevent relative paths to images from failing.
														# when executing the script outside the filepath.
app = wx.App(False)
MainFrame(None, "piDA Graphic Interface")
app.MainLoop()
