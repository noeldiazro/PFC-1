#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

class DataGUI(wx.Panel):
	def __init__(self, parent, mainFrame):
		super(DataGUI,self).__init__(parent,style=wx.NO_BORDER)
		self.parent=parent
		self.mainFrame=mainFrame
		self.InitUI(parent)


	def InitUI(self,parent):
		hbox = wx.BoxSizer(wx.HORIZONTAL)	# horizonal layout
		vbox1 = wx.BoxSizer(wx.VERTICAL) 	#first column (buttons)
		vbox2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Channel #0:"), orient=wx.VERTICAL) 	#second column
		vbox3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Channel #1:"), orient=wx.VERTICAL)		#third column
		vbox4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Channel #2:"), orient=wx.VERTICAL) 	#fourth column
		vbox5 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Channel #3:"), orient=wx.VERTICAL) 	#fifth column



		#First column (Buttons)
		self.BRefreshAllData = wx.BitmapButton(self,-1,wx.Image("./graphics/refresh-button.png",wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		vbox1.Add(self.BRefreshAllData)


		#Second column
		
		self.LCch0 = CustomListCtrl(self)
		self.LCch0.InsertColumn(0,"T (s)")
		self.LCch0.InsertColumn(1,"Valor")
		vbox2.Add(self.LCch0,1,flag=wx.EXPAND)

		#Third column
		self.LCch1 = CustomListCtrl(self)
		self.LCch1.InsertColumn(0,"T (s)")
		self.LCch1.InsertColumn(1,"Valor")
		vbox3.Add(self.LCch1,1,flag=wx.EXPAND)

		#Fourth column
		self.LCch2 = CustomListCtrl(self)
		self.LCch2.InsertColumn(0,"T (s)")
		self.LCch2.InsertColumn(1,"Valor")
		vbox4.Add(self.LCch2,1,flag=wx.EXPAND)

		#Fifth column
		self.LCch3 = CustomListCtrl(self)
		self.LCch3.InsertColumn(0,"T (s)")
		self.LCch3.InsertColumn(1,"Valor")
		vbox5.Add(self.LCch3,1,flag=wx.EXPAND)

		hbox.Add(vbox1)
		hbox.Add(vbox2,1,flag=wx.EXPAND | wx.ALL,border=2)
		hbox.Add(vbox3,1,flag=wx.EXPAND | wx.ALL,border=2)
		hbox.Add(vbox4,1,flag=wx.EXPAND | wx.ALL,border=2)
		hbox.Add(vbox5,1,flag=wx.EXPAND | wx.ALL,border=2)
		self.SetSizer(hbox)




class CustomListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
	def __init__(self, parent):
		wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
		ListCtrlAutoWidthMixin.__init__(self)
		