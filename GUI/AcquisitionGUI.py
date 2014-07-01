#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx
from classes import Simulator

class AcquisitionGUI(wx.Panel):
	def __init__(self, parent):
		super(AcquisitionGUI,self).__init__(parent)
		self.InitUI(parent)

	def InitUI(self,parent):
		self.InitStatusLights()
		# Sizers
		hbox = wx.BoxSizer(wx.HORIZONTAL)	# horizonal layout
		vbox1 = wx.BoxSizer(wx.VERTICAL) 	#first column
		vbox2 = wx.BoxSizer(wx.VERTICAL) 	#second column

		# First column
		#	First row
		hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
		hbox1.Add(wx.StaticText(self, label='Estado: '),flag=wx.ALIGN_LEFT)
		self.statusText = wx.StaticText(self, label='Waiting...')
		hbox1.Add(self.statusText,flag=wx.ALIGN_CENTER)
		self.statusPNG = self.greyLight
		self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(self.statusPNG))
		hbox1.Add(self.imageCtrl,border=10,flag=wx.ALIGN_RIGHT)
		vbox1.Add(hbox1, flag=wx.ALIGN_CENTER)

		vbox1.Add(wx.StaticText(self, label='Frecuencia de muestreo:'),flag=wx.ALIGN_CENTER|wx.TOP,border=10)

		#	Sampling rate row
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		self.samplingRateTCtrl = wx.TextCtrl(self)
		self.SRMeasure = wx.ComboBox(self, choices=["Hz","muestras/seg."],style=wx.CB_READONLY) 
		hbox2.Add(self.samplingRateTCtrl,flag=wx.ALIGN_CENTER)
		hbox2.Add(self.SRMeasure,flag=wx.ALIGN_CENTER)
		vbox1.Add(hbox2,flag=wx.ALIGN_CENTER)

		#	Control buttons
		hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		self.pauseButton=wx.Button(self,label="Pausar")
		self.startButton=wx.Button(self,label="Empezar")
		hbox3.Add(self.pauseButton,flag=wx.EXPAND|wx.ALL,border=10)
		hbox3.Add(self.startButton,flag=wx.EXPAND|wx.ALL,border=10)
		vbox1.Add(hbox3,flag=wx.ALIGN_CENTER)

		#	Simulation button
		self.simButton=wx.Button(self,label="Simulación")
		self.simButton.Bind(wx.EVT_BUTTON, self.simulationClick)
		vbox1.Add(self.simButton,flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=25)

		# Second Column

		self.listCtrl = wx.ListCtrl(self,style=wx.LC_REPORT)
		self.listCtrl.InsertColumn(0,"T (s)")
		self.listCtrl.InsertColumn(1,"Valor")


		# Main sizers arrangements

		hbox.Add(vbox1,1,flag=wx.ALIGN_CENTER|wx.EXPAND)
		hbox.Add(self.listCtrl,3, flag=wx.EXPAND)
		self.SetSizerAndFit(hbox)

	def InitStatusLights(self):
		self.redLight = wx.Image("./graphics/red_light.png",wx.BITMAP_TYPE_PNG).Scale(16,16)
		self.greenLight = wx.Image("./graphics/green_light.png",wx.BITMAP_TYPE_PNG).Scale(16,16)
		self.yellowLight = wx.Image("./graphics/yellow_light.png",wx.BITMAP_TYPE_PNG).Scale(16,16)
		self.greyLight = wx.Image("./graphics/grey_light.png",wx.BITMAP_TYPE_PNG).Scale(16,16)



	#							#
	#	E	V	E	N	T	S	#
	#							#

	def simulationClick(self,event):
		openFileDialog = wx.FileDialog(self, "Abrir fichero CSV", "", "","CSV (*.csv)|*.csv", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		if openFileDialog.ShowModal() == wx.ID_CANCEL:
			return     # the user changed idea...

        # proceed loading the file chosen by the user
        # this can be done with e.g. wxPython input streams:
		self.Module = Simulator.Simulator()
		self.Module.setFileInput(openFileDialog.GetPath())





