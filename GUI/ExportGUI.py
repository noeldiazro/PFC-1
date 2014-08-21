#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

class ExportGUI(wx.Panel):
	def __init__(self, parent, mainFrame):
		super(ExportGUI,self).__init__(parent,style=wx.NO_BORDER)
		self.mainFrame=mainFrame