#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

class DataGUI(wx.Panel):
	def __init__(self, parent, mainFrame):
		super(DataGUI,self).__init__(parent,style=wx.NO_BORDER)
		self.mainFrame=mainFrame
		self.InitUI(parent)


	def InitUI(self,parent):
		hbox = wx.BoxSizer(wx.HORIZONTAL)	# horizonal layout
		vbox1 = wx.BoxSizer(wx.VERTICAL) 	#first column (buttons)
		vbox2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, " Channel #0:"), orient=wx.VERTICAL) 	#second column
		vbox3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, " Channel #1:"), orient=wx.VERTICAL)		#third column
		vbox4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, " Channel #2:"), orient=wx.VERTICAL) 	#fourth column
		vbox5 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, " Channel #3:"), orient=wx.VERTICAL) 	#fifth column



		#First column (Buttons)
		self.BRefreshAllData = wx.BitmapButton(self,-1,wx.Image("./graphics/refresh-data-all.png",wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		self.BRefreshCh0Data = wx.BitmapButton(self,0,wx.Image("./graphics/refresh-data-ch0.png",wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		self.BRefreshCh1Data = wx.BitmapButton(self,1,wx.Image("./graphics/refresh-data-ch1.png",wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		self.BRefreshCh2Data = wx.BitmapButton(self,2,wx.Image("./graphics/refresh-data-ch2.png",wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		self.BRefreshCh3Data = wx.BitmapButton(self,3,wx.Image("./graphics/refresh-data-ch3.png",wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		
		vbox1.Add(self.BRefreshAllData)
		vbox1.Add(self.BRefreshCh0Data)
		vbox1.Add(self.BRefreshCh1Data)
		vbox1.Add(self.BRefreshCh2Data)
		vbox1.Add(self.BRefreshCh3Data)


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
		hbox.Add(vbox2,1,flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.DOWN,border=2)
		hbox.Add(vbox3,1,flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.DOWN,border=2)
		hbox.Add(vbox4,1,flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.DOWN,border=2)
		hbox.Add(vbox5,1,flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.DOWN,border=2)
		self.SetSizer(hbox)

		self.Bind(wx.EVT_BUTTON,self.OnUpdateAll,self.BRefreshAllData)
		self.Bind(wx.EVT_BUTTON,self.OnUpdateChannel)


	def UpdateChannelWidgets(self,channel,enable):
		if(channel==0):
			if(enable):
				self.LCch0.Enable()
				self.BRefreshCh0Data.Enable()
			else:
				self.LCch0.Disable()
				self.BRefreshCh0Data.Disable()
		elif(channel==1):
			if(enable):
				self.LCch1.Enable()
				self.BRefreshCh1Data.Enable()
			else:
				self.LCch1.Disable()
				self.BRefreshCh1Data.Disable()

		elif(channel==2):
			if(enable):
				self.LCch2.Enable()
				self.BRefreshCh2Data.Enable()
			else:
				self.LCch2.Disable()
				self.BRefreshCh2Data.Disable()

		elif(channel==3):
			if(enable):
				self.LCch3.Enable()
				self.BRefreshCh3Data.Enable()
			else:
				self.LCch3.Disable()
				self.BRefreshCh3Data.Disable()




		# # # # # # # # # # # # # #	#
		#							#
		#	E	V	E	N	T	S	#
		#							#
		# # # # # # # # # # # # # #	#


	def OnUpdateAll(self,e):
		if(self.mainFrame.channel_has_input[0]):
			for x in self.mainFrame.acqPanel0.Module.get_data(-self.LCch0.GetItemCount()):
				self.LCch0.Append(x)
		if(self.mainFrame.channel_has_input[1]):
			for x in self.mainFrame.acqPanel1.Module.get_data(-self.LCch1.GetItemCount()):
				self.LCch1.Append(x)
		if(self.mainFrame.channel_has_input[2]):
			for x in self.mainFrame.acqPanel2.Module.get_data(-self.LCch2.GetItemCount()):
				self.LCch2.Append(x)
		if(self.mainFrame.channel_has_input[3]):
			for x in self.mainFrame.acqPanel3.Module.get_data(-self.LCch3.GetItemCount()):
				self.LCch3.Append(x)

	def OnUpdateChannel(self,e):
		if(e.GetId()==0):
			for x in self.mainFrame.acqPanel0.Module.get_data(-self.LCch0.GetItemCount()):
				self.LCch0.Append(x)
		elif(e.GetId()==1):
			for x in self.mainFrame.acqPanel1.Module.get_data(-self.LCch1.GetItemCount()):
				self.LCch1.Append(x)
		elif(e.GetId()==2):
			for x in self.mainFrame.acqPanel2.Module.get_data(-self.LCch2.GetItemCount()):
				self.LCch2.Append(x)
		elif(e.GetId()==3):
			for x in self.mainFrame.acqPanel3.Module.get_data(-self.LCch3.GetItemCount()):
				self.LCch3.Append(x)
		else:
			self.OnUpdateAll(e)


class CustomListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
	def __init__(self, parent):
		wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
		ListCtrlAutoWidthMixin.__init__(self)
		self.setResizeColumn(0)
		