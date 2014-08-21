#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx
from utils.CSVUtils import Writer

class ExportGUI(wx.Panel):
	def __init__(self, parent, mainFrame):
		super(ExportGUI,self).__init__(parent,style=wx.NO_BORDER)
		self.mainFrame=mainFrame
		self.InitUI()


	def InitUI(self):
		vbox = wx.BoxSizer(wx.VERTICAL)	#vertical panel layout
		hbox = wx.BoxSizer(wx.HORIZONTAL)	# horizonal layout for each channel

		vbox1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, " Channel #0:"), orient=wx.VERTICAL) 	#first column
		vbox2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, " Channel #1:"), orient=wx.VERTICAL)	#second column
		vbox3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, " Channel #2:"), orient=wx.VERTICAL) 	#third column
		vbox4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, " Channel #3:"), orient=wx.VERTICAL) 	#fourth column
		
		hbox5 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, " All Channels:"), orient=wx.HORIZONTAL)#last row



		#First column 


		#Second column
		
		

		#Third column
		

		#Fourth column
		

		#Last row
		hbox5.Add(wx.Button(self,-1,"ojete"))

		hbox.Add(vbox1,1,flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.DOWN,border=2)
		hbox.Add(vbox2,1,flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.DOWN,border=2)
		hbox.Add(vbox3,1,flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.DOWN,border=2)
		hbox.Add(vbox4,1,flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.DOWN,border=2)

		vbox.Add(hbox,1,flag=wx.EXPAND)
		vbox.Add(hbox5,0,flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.DOWN,border=2)
		self.SetSizer(vbox)



		# # # # # # # # # # # # # #	#
		#							#
		#	E	V	E	N	T	S	#
		#							#
		# # # # # # # # # # # # # #	#

	def OnExportAll(self,e):
		"""Exports all the data to one file. 
			*NOT FINISHED* *EXAMPLE OF HOW TO EXPORT TO CSV FROM CHANNEL 0 DATA*
		"""
		saveFileDialog = wx.FileDialog(self, "Abrir fichero CSV", "", "","CSV (*.csv)|*.csv", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if saveFileDialog.ShowModal() == wx.ID_CANCEL:
			return     # the user changed idea...
		output = Writer(saveFileDialog.GetPath())
		output.writerows(self.mainFrame.acqPanel0.Module.get_data())
		