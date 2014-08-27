#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx
import threading
from wx.lib import masked
from classes import Simulator
from utils.PointUtils import PointsToDoubleLists
from utils.MatplotlibUtils import *
import matplotlib.lines as lines
import piDA
from piDA.interfaces import piDAInterface
import numpy as np


class AcquisitionGUI(wx.Panel):
	def __init__(self, parent, mainFrame,channel_id):
		super(AcquisitionGUI,self).__init__(parent,style=wx.NO_BORDER)
		self.parent=parent
		self.mainFrame=mainFrame
		self.channel_id = channel_id
		self.plot_color = IntToCharColor(channel_id)
		self.time_offset=0
		self.InitUI(parent)
		self.drawedPoints = 0
		#HW Channel initialization through piDA lib
		inter0 = piDAInterface()
		#This tries to initialize the channel.
		# If it's not available, it will disable the widgets.
		try:	
			ch0 = inter0.get_channel_by_id(channel_id)
			self.Module = piDA.Acquisition(1,ch0)
			self.SetStatusLight("green")
			self.SetStatusText("Ready.")
			self.mainFrame.channel_has_input[channel_id] = True
			self.mainFrame.channel_available[channel_id] = True
		except IndexError:	#Meaning there's no input for this channel.
			self.ToggleWidgets(False)
			self.Module=False
			del inter0

	def InitUI(self,parent):
		self.InitStatusLights()
		
		# Sizers
		text = " Channel #"+str(self.channel_id)+":"
		box = wx.StaticBox(self, wx.ID_ANY, text)
		hbox = wx.BoxSizer(wx.HORIZONTAL)	# horizonal layout
		border = wx.StaticBoxSizer(box, orient=wx.VERTICAL)	# border layout for static box
		vbox1 = wx.BoxSizer(wx.VERTICAL) 	#first column
		vbox2 = wx.BoxSizer(wx.VERTICAL) 	#second column


		#	First row
		hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
		hbox1.Add(wx.StaticText(self, label='Status: '),flag=wx.ALIGN_CENTER)
		self.statusText= wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_CENTRE)
		self.statusText.SetValue("NO INPUT.")
		hbox1.Add(self.statusText,flag=wx.ALIGN_CENTER)
		self.statusPNG = self.greyLight
		self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(self.statusPNG))
		hbox1.Add(self.imageCtrl,border=10,flag=wx.ALIGN_RIGHT)
		vbox1.Add(hbox1, flag=wx.ALIGN_CENTER)

		# Plot color row
		hbox4 = wx.BoxSizer(wx.HORIZONTAL) 
		hbox4.Add(wx.StaticText(self, label='Plot color:'),flag=wx.ALIGN_CENTER|wx.TOP,border=2)
		self.CBPlotColor = wx.ComboBox(self, choices=GetColorList(),style=wx.CB_READONLY,size=wx.Size(100, 20))
		self.CBPlotColor.SetSelection(self.channel_id) 
		self.CBPlotColor.Bind(wx.EVT_COMBOBOX, self.PlotColorComboBox)
		hbox4.Add(self.CBPlotColor,flag=wx.ALIGN_CENTER|wx.TOP,border=2)
		vbox1.Add(hbox4,flag=wx.ALIGN_CENTER)

		# Sampling rate text
		vbox1.Add(wx.StaticText(self, label='Sampling rate:'),flag=wx.ALIGN_CENTER|wx.TOP,border=2)

		# And sampling rate row
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		self.samplingRateTCtrl = masked.NumCtrl(self, value=1, fractionWidth=0, allowNegative=False, min=0, max=10000,autoSize=False)
		self.samplingRateTCtrl.Bind(wx.EVT_TEXT, self.SamplingRateTextCtrl)
		self.SRMeasure = wx.ComboBox(self, choices=["Hz"],style=wx.CB_READONLY,size=wx.Size(100, 20))
		self.SRMeasure.SetSelection(0) 
		self.SRMeasure.Bind(wx.EVT_COMBOBOX, self.SamplingRateComboBox)
		hbox2.Add(self.samplingRateTCtrl,flag=wx.ALIGN_CENTER)
		hbox2.Add(self.SRMeasure,flag=wx.ALIGN_CENTER)
		vbox1.Add(hbox2,flag=wx.ALIGN_CENTER)


		#	Control buttons
		hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		self.pauseButton=wx.Button(self,label="Stop")
		self.pauseButton.Disable()		# You can't stop something that hasn't started.
		self.startButton=wx.Button(self,label="Start")
		self.pauseButton.Bind(wx.EVT_BUTTON,self.StopClick)
		self.startButton.Bind(wx.EVT_BUTTON,self.StartClick)
		hbox3.Add(self.pauseButton,flag=wx.ALIGN_CENTER|wx.ALL,border=5)
		hbox3.Add(self.startButton,flag=wx.ALIGN_CENTER|wx.ALL,border=5)
		vbox1.Add(hbox3,flag=wx.ALIGN_CENTER)

		#	Simulation button
		self.simButton=wx.Button(self,label="Simulation")
		self.simButton.Bind(wx.EVT_BUTTON, self.SimulationClick)
		vbox1.Add(self.simButton,flag=wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, border=50)

		# Main sizers arrangements

		border.Add(vbox1,1,flag=wx.ALIGN_CENTER|wx.EXPAND)
		hbox.Add(border,1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=2)
		self.SetSizerAndFit(hbox)
		
	"""
		Initializes all the posible light colors.
	"""
	def InitStatusLights(self):
		self.redLight = wx.Image("./graphics/red_light.png",wx.BITMAP_TYPE_PNG).Scale(16,16)
		self.greenLight = wx.Image("./graphics/green_light.png",wx.BITMAP_TYPE_PNG).Scale(16,16)
		self.yellowLight = wx.Image("./graphics/yellow_light.png",wx.BITMAP_TYPE_PNG).Scale(16,16)
		self.greyLight = wx.Image("./graphics/grey_light.png",wx.BITMAP_TYPE_PNG).Scale(16,16)

	""" 
		Changes status light for the panel and returns old bitmap.
	"""
	def SetStatusLight(self,inp):
		old = self.imageCtrl.GetBitmap()
		# if type is wx.Bitmap we show it rightaway
		if type(inp) is wx.Bitmap:
			self.imageCtrl.SetBitmap(inp)
			return old
		#if is a string with the desired color, we need to convert and use the
		#	initialized lights.
		if inp=="red":
			self.imageCtrl.SetBitmap(wx.BitmapFromImage(self.redLight))
		elif inp=="green":
			self.imageCtrl.SetBitmap(wx.BitmapFromImage(self.greenLight))
		elif inp=="yellow":
			self.imageCtrl.SetBitmap(wx.BitmapFromImage(self.yellowLight))
		else:
			self.imageCtrl.SetBitmap(wx.BitmapFromImage(self.greyLight))
		return old

	"""
		Changes status text for the panel and returns old text.
	"""
	def SetStatusText(self,text):
				old = self.statusText.GetValue()
				self.statusText.ChangeValue(text)
				return old

	"""
		Disables widgets so the user won't mess up anything clicking when he's not supposed to.
		TODO
	"""
	def ToggleWidgets(self,status):
		if status==False:
			self.samplingRateTCtrl.Disable()
			self.SRMeasure.Disable()
			self.startButton.Disable()
			self.pauseButton.Disable()
			self.simButton.Disable()
			self.CBPlotColor.Disable()
			
		else:
			self.samplingRateTCtrl.Enable()
			self.SRMeasure.Enable()
			self.startButton.Enable()
			self.pauseButton.Enable()
			self.simButton.Enable()
			self.CBPlotColor.Enable()
	
	"""
		Writes the lines read by the Module into the Axes in MainFrame
	"""
	def PushData(self):
		try:

			with self.Module.LOCK:
				# piDA allows us to ask for the number of points we want to retrieve. 
				#	In order to trick the lib we need to pass the "minus drawed points":
				lists = PointsToDoubleLists(self.Module.get_data(-self.drawedPoints))
			
			self.mainFrame.line1.set_xdata(np.append(self.mainFrame.line1.get_xdata(),[x+self.time_offset for x in lists[0]]))
			self.mainFrame.line1.set_ydata(np.append(self.mainFrame.line1.get_ydata(),lists[1]))
			self.mainFrame.line1.set_color(self.plot_color)
			self.mainFrame.axes1.draw_artist(self.mainFrame.line1)
			
			self.drawedPoints=self.drawedPoints+len(lists[0])

		except RuntimeError as inst:
			print type(inst)     # the exception instance
			print inst.args      # arguments stored in .args
			print inst           # __str__ allows args to printed directly
			print len(self.Module.data.x)
			print len(self.Module.data.y)


	#							#
	#	E	V	E	N	T	S	#
	#							#

	def SimulationClick(self,event):
		oldLight = self.SetStatusLight("yellow")
		oldText = self.SetStatusText("Busy...")
		self.ToggleWidgets(False)
		openFileDialog = wx.FileDialog(self, "Abrir fichero CSV", "", "","CSV (*.csv)|*.csv", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		if openFileDialog.ShowModal() == wx.ID_CANCEL:
			self.SetStatusLight(oldLight)
			self.SetStatusText(oldText)
			self.ToggleWidgets(True)
			return     # the user changed idea...

		# proceed loading the file chosen by the user
		# this can be done with e.g. wxPython input streams:
		self.Module = Simulator.Simulator(self.samplingRateTCtrl.GetValue())
		self.Module.setFileInput(openFileDialog.GetPath())
		self.SetStatusLight("red")
		self.SetStatusText("Ready.")
		event.GetEventObject().SetLabel(openFileDialog.GetFilename())
		self.ToggleWidgets(True)

	def StartClick(self,event):
		self.startButton.Disable()
		self.simButton.Disable()
		self.Module.start()
		self.SetStatusText("Active.")
		self.SetStatusLight("yellow")
		self.mainFrame.channel_active[self.channel_id]=True
		self.mainFrame.channel_available[self.channel_id]=False
		self.mainFrame.ToggleGraphRefreshing(check_channels=True)

		#Offset calc:
		if(self.mainFrame.master_channel):
			#Prints for debugging purposes
			self.Module.start_time_lock.acquire()	# We have to wait for start_time to initialize in
													#	the Acquisition Module thread before going on
			self.time_offset=(self.Module.start_time-self.mainFrame.master_channel.start_time)
			#print self.time_offset
		else:
			self.mainFrame.set_master_module(self.Module)
		self.pauseButton.Enable()
		self.mainFrame.disableStartAllButton()

	def StopClick(self,e):
		self.ToggleWidgets(False)
		self.Module.stop()
		self.mainFrame.channel_active[self.channel_id]=False
		self.SetStatusLight("yellow")
		self.SetStatusText("Busy...")
		t = threading.Thread(target=self._updateStoppedStatus)
		t.daemon=True
		t.start()
		self.mainFrame.ToggleGraphRefreshing(check_channels=True)

	def _updateStoppedStatus(self):
		while(self.Module.get_status()=='running'):
			pass
		if(self.Module.get_status()=='stopped'):
			self.SetStatusText("Stopped.")
			self.SetStatusLight("red")
		else:
			self.startButton.Enable()
			self.SetStatusText("Paused.")
			self.SetStatusLight("green")

	def SamplingRateTextCtrl(self,event):
		if self.Module:
			self.Module.sampling_rate = int(self.samplingRateTCtrl.GetValue())
		
	def PlotColorComboBox(self,event):
		self.plot_color = IntToCharColor(event.GetEventObject().GetSelection())

	def SamplingRateComboBox(self,event):
		pass




