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
		hbox11 = wx.BoxSizer(wx.HORIZONTAL)
		self.TC1title= wx.TextCtrl(self)
		self.TC1title.SetValue(self.mainFrame.get_plot_title())
		hbox11.Add(wx.StaticText(self,-1,"Title:	"),flag=wx.ALIGN_LEFT| wx.ALL,border=1)
		hbox11.Add(self.TC1title,flag=wx.ALIGN_RIGHT)

		hbox12 = wx.BoxSizer(wx.HORIZONTAL)
		self.TCx1Label= wx.TextCtrl(self)
		self.TCx1Label.SetValue(self.mainFrame.get_xlabel())
		hbox12.Add(wx.StaticText(self,-1,"X Label:	"),flag=wx.ALIGN_LEFT| wx.ALL,border=1)
		hbox12.Add(self.TCx1Label,flag=wx.ALIGN_RIGHT)

		hbox13 = wx.BoxSizer(wx.HORIZONTAL)
		self.TCy1Label= wx.TextCtrl(self)
		self.TCy1Label.SetValue(self.mainFrame.get_ylabel())
		hbox13.Add(wx.StaticText(self,-1,"Y Label:	"),flag=wx.ALIGN_LEFT| wx.ALL,border=1)
		hbox13.Add(self.TCy1Label,flag=wx.ALIGN_RIGHT)

		hbox14 = wx.BoxSizer(wx.HORIZONTAL)
		self.BcsvCh0 = wx.Button(self,0,"Export CSV")
		self.BpdfCh0 = wx.Button(self,-1,"Export PDF")
		hbox14.Add(self.BcsvCh0,flag=wx.ALIGN_CENTER|wx.ALL,border=1)
		hbox14.Add(self.BpdfCh0,flag=wx.ALIGN_CENTER|wx.ALL,border=1)


		vbox1.Add(hbox11,flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		vbox1.Add(hbox12,flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		vbox1.Add(hbox13,flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		vbox1.Add(hbox14,flag=wx.ALIGN_CENTER | wx.ALL,border=1)

		#Second column
		hbox21 = wx.BoxSizer(wx.HORIZONTAL)
		self.TC2title= wx.TextCtrl(self)
		self.TC2title.SetValue(self.mainFrame.get_plot_title())
		hbox21.Add(wx.StaticText(self,-1,"Title:	"),flag=wx.ALIGN_LEFT| wx.ALL,border=1)
		hbox21.Add(self.TC2title,flag=wx.ALIGN_RIGHT)

		hbox22 = wx.BoxSizer(wx.HORIZONTAL)
		self.TCx2Label= wx.TextCtrl(self)
		self.TCx2Label.SetValue(self.mainFrame.get_xlabel())
		hbox22.Add(wx.StaticText(self,-1,"X Label:	"),flag=wx.ALIGN_LEFT| wx.ALL,border=1)
		hbox22.Add(self.TCx2Label,flag=wx.ALIGN_RIGHT)

		hbox23 = wx.BoxSizer(wx.HORIZONTAL)
		self.TCy2Label= wx.TextCtrl(self)
		self.TCy2Label.SetValue(self.mainFrame.get_ylabel())
		hbox23.Add(wx.StaticText(self,-1,"Y Label:	"),flag=wx.ALIGN_LEFT| wx.ALL,border=1)
		hbox23.Add(self.TCy2Label,flag=wx.ALIGN_RIGHT)

		hbox24 = wx.BoxSizer(wx.HORIZONTAL)
		self.BcsvCh1 = wx.Button(self,1,"Export CSV")
		self.BpdfCh1 = wx.Button(self,-1,"Export PDF")
		hbox24.Add(self.BcsvCh1,flag=wx.ALIGN_CENTER|wx.ALL,border=1)
		hbox24.Add(self.BpdfCh1,flag=wx.ALIGN_CENTER|wx.ALL,border=1)


		vbox2.Add(hbox21,flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		vbox2.Add(hbox22,flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		vbox2.Add(hbox23,flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		vbox2.Add(hbox24,flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		

		#Third column
		hbox31 = wx.BoxSizer(wx.HORIZONTAL)
		self.TC3title= wx.TextCtrl(self)
		self.TC3title.SetValue(self.mainFrame.get_plot_title())
		hbox31.Add(wx.StaticText(self,-1,"Title:	"),flag=wx.ALIGN_LEFT| wx.ALL,border=1)
		hbox31.Add(self.TC3title,flag=wx.ALIGN_RIGHT)

		hbox32 = wx.BoxSizer(wx.HORIZONTAL)
		self.TCx3Label= wx.TextCtrl(self)
		self.TCx3Label.SetValue(self.mainFrame.get_xlabel())
		hbox32.Add(wx.StaticText(self,-1,"X Label:	"),flag=wx.ALIGN_LEFT| wx.ALL,border=1)
		hbox32.Add(self.TCx3Label,flag=wx.ALIGN_RIGHT)

		hbox33 = wx.BoxSizer(wx.HORIZONTAL)
		self.TCy3Label= wx.TextCtrl(self)
		self.TCy3Label.SetValue(self.mainFrame.get_ylabel())
		hbox33.Add(wx.StaticText(self,-1,"Y Label:	"),flag=wx.ALIGN_LEFT| wx.ALL,border=1)
		hbox33.Add(self.TCy3Label,flag=wx.ALIGN_RIGHT)

		hbox34 = wx.BoxSizer(wx.HORIZONTAL)
		self.BcsvCh2 = wx.Button(self,2,"Export CSV")
		self.BpdfCh2 = wx.Button(self,-1,"Export PDF")
		hbox34.Add(self.BcsvCh2,flag=wx.ALIGN_CENTER|wx.ALL,border=1)
		hbox34.Add(self.BpdfCh2,flag=wx.ALIGN_CENTER|wx.ALL,border=1)


		vbox3.Add(hbox31,flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		vbox3.Add(hbox32,flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		vbox3.Add(hbox33,flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		vbox3.Add(hbox34,flag=wx.ALIGN_CENTER | wx.ALL,border=1)

		#Fourth column
		hbox41 = wx.BoxSizer(wx.HORIZONTAL)
		self.TC4title= wx.TextCtrl(self)
		self.TC4title.SetValue(self.mainFrame.get_plot_title())
		hbox41.Add(wx.StaticText(self,-1,"Title:	"),flag=wx.ALIGN_LEFT| wx.ALL,border=1)
		hbox41.Add(self.TC4title,flag=wx.ALIGN_RIGHT)

		hbox42 = wx.BoxSizer(wx.HORIZONTAL)
		self.TCx4Label= wx.TextCtrl(self)
		self.TCx4Label.SetValue(self.mainFrame.get_xlabel())
		hbox42.Add(wx.StaticText(self,-1,"X Label:	"),flag=wx.ALIGN_LEFT| wx.ALL,border=1)
		hbox42.Add(self.TCx4Label,flag=wx.ALIGN_RIGHT)

		hbox43 = wx.BoxSizer(wx.HORIZONTAL)
		self.TCy4Label= wx.TextCtrl(self)
		self.TCy4Label.SetValue(self.mainFrame.get_ylabel())
		hbox43.Add(wx.StaticText(self,-1,"Y Label:	"),flag=wx.ALIGN_LEFT| wx.ALL,border=1)
		hbox43.Add(self.TCy4Label,flag=wx.ALIGN_RIGHT)

		hbox44 = wx.BoxSizer(wx.HORIZONTAL)
		self.BcsvCh3 = wx.Button(self,3,"Export CSV")
		self.BpdfCh3 = wx.Button(self,-1,"Export PDF")
		hbox44.Add(self.BcsvCh3,flag=wx.ALIGN_CENTER|wx.ALL,border=1)
		hbox44.Add(self.BpdfCh3,flag=wx.ALIGN_CENTER|wx.ALL,border=1)


		vbox4.Add(hbox41,flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		vbox4.Add(hbox42,flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		vbox4.Add(hbox43,flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		vbox4.Add(hbox44,flag=wx.ALIGN_CENTER | wx.ALL,border=1)

		#Last row

		self.BcsvAll = wx.Button(self,-1,"Export to CSV")
		self.BpdfAll = wx.Button(self,-1,"Export to PDF")

		self.cbCh0 = wx.CheckBox(self,label="Ch0")
		self.cbCh1 = wx.CheckBox(self,label="Ch1")
		self.cbCh2 = wx.CheckBox(self,label="Ch2")
		self.cbCh3 = wx.CheckBox(self,label="Ch3")

		self.cbCh0.SetValue(True)
		self.cbCh1.SetValue(True)
		self.cbCh2.SetValue(True)
		self.cbCh3.SetValue(True)

		self.CBXMerge = wx.ComboBox(self, choices=["s (1)","ms (0.001)","ns (0.00001)","us (0.000000001)"],style=wx.CB_READONLY,size=wx.Size(100, 20))
		self.CBXMerge.SetSelection(0)

		hbox5.Add(wx.StaticText(self,label="Select channels: "),flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		hbox5.Add(self.cbCh0,flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		hbox5.Add(self.cbCh1,flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		hbox5.Add(self.cbCh2,flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		hbox5.Add(self.cbCh3,flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		hbox5.Add(self.CBXMerge,flag=wx.ALIGN_CENTER | wx.ALL,border=1)
		hbox5.Add(self.BcsvAll,flag=wx.ALIGN_CENTER | wx.ALL,border=3)
		hbox5.Add(self.BpdfAll,flag=wx.ALIGN_CENTER | wx.ALL,border=3)

		# Sizers

		hbox.Add(vbox1,1,flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.DOWN,border=2)
		hbox.Add(vbox2,1,flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.DOWN,border=2)
		hbox.Add(vbox3,1,flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.DOWN,border=2)
		hbox.Add(vbox4,1,flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.DOWN,border=2)

		vbox.Add(hbox,1,flag=wx.EXPAND)
		vbox.Add(hbox5,0,flag=wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT | wx.DOWN,border=2)
		self.SetSizer(vbox)

		#Bindings

		self.BcsvCh0.Bind(wx.EVT_BUTTON,self.OnExportChannelToCSV)
		self.BcsvCh1.Bind(wx.EVT_BUTTON,self.OnExportChannelToCSV)
		self.BcsvCh2.Bind(wx.EVT_BUTTON,self.OnExportChannelToCSV)
		self.BcsvCh3.Bind(wx.EVT_BUTTON,self.OnExportChannelToCSV)



	def SaveFileDialog(self):
		"""Opens a File Dialog for file saving and returns the file path chosen"""
		saveFileDialog = wx.FileDialog(self, "Export as CSV", "", "","CSV (*.csv)|*.csv", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if saveFileDialog.ShowModal() == wx.ID_CANCEL:
			return     # the user changed idea...
		filepath = saveFileDialog.GetPath()
		#This conditional checks if the file extension was added to the filename.
		if filepath[-4:].lower() != ".csv":
			filepath += ".csv"
		return filepath

	def UpdateChannelWidgets(self,channel,enable):
		if(channel==0):
			if(enable):
				self.TC1title.Enable()
				self.TCx1Label.Enable()
				self.TCy1Label.Enable()
				self.BcsvCh0.Enable()
				self.BpdfCh0.Enable()
				self.cbCh0.Enable()
			else:
				self.TC1title.Disable()
				self.TCx1Label.Disable()
				self.TCy1Label.Disable()
				self.BcsvCh0.Disable()
				self.BpdfCh0.Disable()
				self.cbCh0.SetValue(False)
				self.cbCh0.Disable()
		elif(channel==1):
			if(enable):
				self.TC2title.Enable()
				self.TCx2Label.Enable()
				self.TCy2Label.Enable()
				self.BcsvCh1.Enable()
				self.BpdfCh1.Enable()
				self.cbCh1.Enable()
			else:
				self.TC2title.Disable()
				self.TCx2Label.Disable()
				self.TCy2Label.Disable()
				self.BcsvCh1.Disable()
				self.BpdfCh1.Disable()
				self.cbCh1.SetValue(False)
				self.cbCh1.Disable()
		elif(channel==2):
			if(enable):
				self.TC3title.Enable()
				self.TCx3Label.Enable()
				self.TCy3Label.Enable()
				self.BcsvCh2.Enable()
				self.BpdfCh2.Enable()
				self.cbCh2.Enable()
			else:
				self.TC3title.Disable()
				self.TCx3Label.Disable()
				self.TCy3Label.Disable()
				self.BcsvCh2.Disable()
				self.BpdfCh2.Disable()
				self.cbCh2.SetValue(False)
				self.cbCh2.Disable()
		elif(channel==3):
			if(enable):
				self.TC4title.Enable()
				self.TCx4Label.Enable()
				self.TCy4Label.Enable()
				self.BcsvCh3.Enable()
				self.BpdfCh3.Enable()
				self.cbCh3.Enable()
			else:
				self.TC4title.Disable()
				self.TCx4Label.Disable()
				self.TCy4Label.Disable()
				self.BcsvCh3.Disable()
				self.BpdfCh3.Disable()
				self.cbCh3.SetValue(False)
				self.cbCh3.Disable()

		#PDF export won't be available for a while, so no point to enable the button
		self.BpdfCh0.Disable()
		self.BpdfCh1.Disable()
		self.BpdfCh2.Disable()
		self.BpdfCh3.Disable()

		#Export all data isn't available just yet...
		self.BpdfAll.Disable()
		self.BcsvAll.Disable()



		# # # # # # # # # # # # # #	#
		#							#
		#	E	V	E	N	T	S	#
		#							#
		# # # # # # # # # # # # # #	#

	def OnExportAll(self,e):
		"""Exports all the data to one file. 
			TODO
		"""
		pass

	def OnExportChannelToCSV(self,e):
		"""Exports channel data to a csv file."""
		filepath = self.SaveFileDialog()
		if filepath=="":
			return
		output = Writer(filepath)
		if (e.GetId() == 0):
			output.writerow([self.TC1title.GetValue()])
			output.writerow([self.TCx1Label.GetValue(),self.TCy1Label.GetValue()])
			output.writerows(self.mainFrame.acqPanel0.Module.get_data())
		elif (e.GetId() == 1):
			output.writerow([self.TC2title.GetValue()])
			output.writerow([self.TCx2Label.GetValue(),self.TCy2Label.GetValue()])
			output.writerows(self.mainFrame.acqPanel1.Module.get_data())
		elif (e.GetId() == 2):
			output.writerow([self.TC3title.GetValue()])
			output.writerow([self.TCx3Label.GetValue(),self.TCy3Label.GetValue()])
			output.writerows(self.mainFrame.acqPanel2.Module.get_data())
		elif (e.GetId() == 3):
			output.writerow([self.TC4title.GetValue()])
			output.writerow([self.TCx4Label.GetValue(),self.TCy4Label.GetValue()])
			output.writerows(self.mainFrame.acqPanel3.Module.get_data())
