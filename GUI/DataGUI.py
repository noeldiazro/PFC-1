#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx

class DataGUI(wx.Panel):
	def __init__(self, parent, mainFrame):
		super(DataGUI,self).__init__(parent,style=wx.NO_BORDER)
		self.parent=parent
		self.mainFrame=mainFrame
		self.InitUI(parent)


	def InitUI(self,parent):
		hbox = wx.BoxSizer(wx.HORIZONTAL)	# horizonal layout
		vbox1 = wx.BoxSizer(wx.VERTICAL) 	#first column (buttons)
		vbox2 = wx.BoxSizer(wx.VERTICAL) 	#second column
		vbox3 = wx.BoxSizer(wx.VERTICAL) 	#third column
		vbox4 = wx.BoxSizer(wx.VERTICAL) 	#fourth column
		vbox5 = wx.BoxSizer(wx.VERTICAL) 	#fifth column



		#First column (Buttons)
		self.BRefreshAllData = wx.BitmapButton(self,-1,wx.Image("./graphics/refresh-button.png",wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		vbox1.Add(self.BRefreshAllData)


		#Second column
		self.LCch0 = wx.ListCtrl(self,style=wx.LC_REPORT)
		self.LCch0.InsertColumn(0,"T (s)")
		self.LCch0.InsertColumn(1,"Valor")
		vbox2.Add(self.LCch0,1,flag=wx.EXPAND | wx.LEFT | wx.RIGHT,border=1)

		#Third column
		self.LCch1 = wx.ListCtrl(self,style=wx.LC_REPORT)
		self.LCch1.InsertColumn(0,"T (s)")
		self.LCch1.InsertColumn(1,"Valor")
		vbox3.Add(self.LCch1,1,flag=wx.EXPAND | wx.LEFT | wx.RIGHT,border=1)

		#Fourth column
		self.LCch2 = wx.ListCtrl(self,style=wx.LC_REPORT)
		self.LCch2.InsertColumn(0,"T (s)")
		self.LCch2.InsertColumn(1,"Valor")
		vbox4.Add(self.LCch2,1,flag=wx.EXPAND | wx.LEFT | wx.RIGHT,border=1)

		#Fifth column
		self.LCch3 = wx.ListCtrl(self,style=wx.LC_REPORT)
		self.LCch3.InsertColumn(0,"T (s)")
		self.LCch3.InsertColumn(1,"Valor")
		vbox5.Add(self.LCch3,1,flag=wx.EXPAND | wx.LEFT | wx.RIGHT,border=1)

		hbox.Add(vbox1)
		hbox.Add(vbox2,1,flag=wx.EXPAND)
		hbox.Add(vbox3,1,flag=wx.EXPAND)
		hbox.Add(vbox4,1,flag=wx.EXPAND)
		hbox.Add(vbox5,1,flag=wx.EXPAND)
		self.SetSizer(hbox)
		