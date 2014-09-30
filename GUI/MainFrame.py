#!/usr/bin/python
# -*- coding: utf-8 -*-

# border.py

import os
import wx
import wx.aui
import matplotlib as mpl
from GUI.AcquisitionGUI import AcquisitionGUI
from GUI.DataGUI import DataGUI
from GUI.ExportGUI import ExportGUI
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
from threading import Thread
import time




class MainFrame(wx.Frame):

	def __init__(self, parent, title):
		super(MainFrame, self).__init__(parent, title=title, 
			size=(1024, 768))
			
		#Variables used by the graph control
		self.update_frequency = 1
		self.autoscale = False
		self.channel_has_input = [False, False, False, False]	#Channel has an available input.
		self.channel_active = [False, False ,False ,False]		#Channel is currently acquiring data.
		self.channel_available = [False, False, False, False]	#Channel is available to acquire data.
		self.master_channel = False
		self.__graphRefreshing=False


		self.InitUI()
		self.Centre()
		self.SetMinSize(wx.Size(1024,480))
		self.Maximize()
		self.Show()
		
	def InitUI(self):
		self.dirname=''
		self.statusbar=self.CreateStatusBar() # A Statusbar in the bottom of the window
		# Setting up the menu.
		fileMenu = wx.Menu()
		viewMenu = wx.Menu()
		helpMenu = wx.Menu()
		menuOpen = fileMenu.Append(wx.ID_OPEN, "&Open Session","Open a saved session")
		menuExit = fileMenu.Append(wx.ID_EXIT,"&Exit","Exit the program")
		
		#View menu structure partially DISABLED
		vm_updateFreqSM = wx.Menu()

		#vm_ufsm_autos = vm_updateFreqSM.Append(5, "Autoscale",kind=wx.ITEM_CHECK)
		
		viewMenu.AppendSubMenu(vm_updateFreqSM,"Plot settings")

		menuHelp= helpMenu.Append(wx.ID_HELP, "&Help","General help")
		menuAbout= helpMenu.Append(wx.ID_ABOUT, "&About","About this program")

		# Creating the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu,"&File") # Adding the "fileMenu" to the MenuBar
		menuBar.Append(viewMenu,"&View")
		menuBar.Append(helpMenu,"&Help")
		self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.



		vbox = wx.BoxSizer(wx.VERTICAL)

		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)

		## hbox1
		# EXAMPLE PLOT
		self.page = Plot(self)
		self.axes = self.page.figure.gca()
		self.axes.set_ylabel("v")
		self.axes.set_xlabel("t (s)")
		self.axes.set_xlim(right=300)
		self.axes.set_ylim(bottom=-0.5,top=5)
		self.line = []
		styles = ['b-','g-','r-','c-']

		# We create the plot lines/artists where data is going to be drawn.
		for s,i in zip(styles,range(4)):
			self.line.append(self.axes.plot([],[],s)[0])
		self.page.canvas.draw()
		#

		## hbox2


		self.nb = wx.aui.AuiNotebook(self,style=wx.aui.AUI_NB_TOP)

		# TEST PANELS
		self.acquisitionPage = wx.Panel(self)
		apshbox = wx.BoxSizer(wx.HORIZONTAL)


		self.acqPanel0 = AcquisitionGUI(self.acquisitionPage,self,0)
		self.acqPanel1 = AcquisitionGUI(self.acquisitionPage,self,1)
		self.acqPanel2 = AcquisitionGUI(self.acquisitionPage,self,2)
		self.acqPanel3 = AcquisitionGUI(self.acquisitionPage,self,3)
		apshbox.Add(self.acqPanel0,1,flag=wx.EXPAND)
		apshbox.Add(self.acqPanel1,1,flag=wx.EXPAND)
		apshbox.Add(self.acqPanel2,1,flag=wx.EXPAND)
		apshbox.Add(self.acqPanel3,1,flag=wx.EXPAND)
		self.acquisitionPage.SetSizer(apshbox)

		self.DataPage = DataGUI(self.nb,self)

		self.ExportPage = ExportGUI(self.nb,self)

		self.nb.AddPage(self.acquisitionPage,"Acquisition")
		self.nb.AddPage(self.DataPage,"Data")
		self.nb.AddPage(self.ExportPage,"Export")
		self.nb.SetMinSize(wx.Size(1024,210))

		vbox.Add(self.page, 1, flag=wx.EXPAND)
		vbox.Add(self.nb, 0, flag=wx.EXPAND | wx.ALL)

		

		self.SetSizer(vbox)


		# Events.
		#self.Bind(wx.EVT_MENU, self.SetUpdateFrequency,vm_ufsm_autos)
		#self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		
		self.Bind(wx.EVT_BUTTON,self.OnStartAll,self.page.BStartAll)
		self.Bind(wx.EVT_BUTTON,self.OnStopAll,self.page.BStopAll)
		self.Bind(wx.EVT_BUTTON,self.OnRefreshAll,self.page.BRefreshAll)
		self.Bind(wx.EVT_SLIDER,self.SetUpdateFrequency,self.page.sld_updFreq)
		self.Bind(wx.EVT_TOGGLEBUTTON,self.OnTBAutomaticUpdate,self.page.TBGraphRefreshing)

		#Updates GUI channel inputs.
		self.UpdateChannelInputs()

	def UpdateChannelInputs(self):
		"""	Updates GUI elements according to the available inputs using UpdateChannelWidgets function in each case"""
		self.DataPage.UpdateChannelWidgets(0,self.channel_has_input[0])
		self.ExportPage.UpdateChannelWidgets(0,self.channel_has_input[0])

		self.DataPage.UpdateChannelWidgets(1,self.channel_has_input[1])
		self.ExportPage.UpdateChannelWidgets(1,self.channel_has_input[1])

		self.DataPage.UpdateChannelWidgets(2,self.channel_has_input[2])
		self.ExportPage.UpdateChannelWidgets(2,self.channel_has_input[2])

		self.DataPage.UpdateChannelWidgets(3,self.channel_has_input[3])
		self.ExportPage.UpdateChannelWidgets(3,self.channel_has_input[3])


	def ToggleGraphRefreshing(self,check_channels=False):
		"""	Toggles automatic graph refreshing with an option to check if there are channels still active. """
		if(check_channels and not any(self.channel_active) and not any(self.channel_available)):
			self.page.BStopAll.Disable()
		# We don't want to stop the graph refreshing if the call comes from a stopping channel
		#	and there are other channels still active.
		if(check_channels and any(self.channel_active) and self.__graphRefreshing):
			return
		# If we don't want to check the active channels, want to start/stop 'immediately' graph refreshing
		#	or last conditional was false, we check current status and invert it.
		if self.__graphRefreshing:
			self.__graphRefreshing=False
			self.statusbar.PushStatusText("Graph Refreshing OFF.")
		elif self.page.TBGraphRefreshing.GetValue():	#TBGraphRefreshing is the main switch for ON/OFF status.
			self.__graphRefreshing=True
			t = Thread(target=self.RefreshGraphLoop)
			t.daemon=True
			t.start()
			self.statusbar.PushStatusText("Graph Refreshing ON.")

	def RefreshGraphLoop(self):
		"""Loop implementing every channel data pulling, plot redrawing and sleeping time"""
		while (self.__graphRefreshing):
			#	First we sleep the update frequency. This will give time to the interface
			# to gather some data too.
			if (self.update_frequency>0):
				time.sleep(self.update_frequency)
			# Then we refresh the graph once.
			self.RefreshGraphOnce()

	def RefreshGraphOnce(self):
		"""Implementing ONCE every channel data pulling, plot redrawing"""
		if(self.master_channel):
			self.page.canvas.restore_region(self.axes_background)
		# Pushes data for each channel if has an input and is active or it was:
		if((self.channel_active[0] or not self.channel_available[0]) and self.channel_has_input[0]):
			self.acqPanel0.PushData();
		if((self.channel_active[1] or not self.channel_available[1]) and self.channel_has_input[1]):
			self.acqPanel1.PushData();
		if((self.channel_active[2] or not self.channel_available[2]) and self.channel_has_input[2]):
			self.acqPanel2.PushData();
		if((self.channel_active[3] or not self.channel_available[3]) and self.channel_has_input[3]):
			self.acqPanel3.PushData();
		# We call ReDraw as a CallAfter as this function makes the call in the main GUI thread.
		wx.CallAfter(self.ReDrawPlot)
		#if self.autoscale:
		#	self.axes.autoscale()

	def ReDrawPlot(self):
		"""Invokes plot redrawing"""
		self.page.canvas.blit(self.axes.bbox)
		#self.page.canvas.draw()

	def set_xlabel(self,label):
		"""Sets the plot x axis label"""
		self.axes.set_xlabel(label)

	def get_xlabel(self):
		"""Gets the plot x axis label"""
		return self.axes.get_xlabel()

	def set_ylabel(self,label):
		"""Sets the plot y axis label"""
		self.axes.set_ylabel(label)
	def get_ylabel(self):
		"""Gets the plot y axis label"""
		return self.axes.get_ylabel()

	def set_plot_title(self,title):
		"""Sets the plot title"""
		self.axes.set_title(title)

	def get_plot_title(self):
		"""Gets the plot title"""
		return self.axes.get_title()

	def set_master_module(self,module):
		"""Sets the master module, usually the module which started first"""
		if not(self.master_channel):
			self.axes_background = self.page.canvas.copy_from_bbox(self.axes.bbox)
			self.master_channel=module


	def all_channels_active(self):
		"""Returns if every channel available is active."""
		return sum(self.channel_active)==sum(self.channel_has_input)

	def disableStartAllButton(self):
		"""Disables StartAll Button if useless"""
		if self.all_channels_active():
			self.page.BStartAll.Disable()

	#							#
	#	E	V	E	N	T	S	#
	#							#
		

	def OnAbout(self,e):
		# Create a message dialog box
		dlg = wx.MessageDialog(self, "End of Degree Project \n Diego Muñoz Callejo, Universidad de Cantabria \n https://github.com/dmcelectrico/PFC", "Acerca de", wx.OK)
		dlg.ShowModal() # Shows it
		dlg.Destroy() # finally destroy it when finished.

	def OnExit(self,e):
		self.Close(True)  # Close the frame.
		exit()

	def OnOpen(self,e):
		""" Open a file """
		dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			f = open(os.path.join(self.dirname, self.filename), 'r')

			f.close()
		dlg.Destroy()

	def SetUpdateFrequency(self,e):
		#If event comes from the slider.
		if (e.GetEventType() == wx.EVT_SLIDER.typeId):
			sld = e.GetEventObject()
			self.update_frequency=sld.GetValue()
			return
		id=e.GetId()
		if id==1:
			self.update_frequency=2
			self.page.sld_updFreq.SetValue(2)
		elif id==2:
			self.update_frequency=5
			self.page.sld_updFreq.SetValue(5)
		elif id==3:
			self.update_frequency=10
			self.page.sld_updFreq.SetValue(10)
		elif id==4:
			self.page.TBGraphRefreshing.SetValue(False)
			self.OnTBAutomaticUpdate
			return
		elif id==5:
			self.autoscale = e.GetEventObject().IsChecked(5)
			return
			# Turns on graphRefreshing if any frequency other than -1 is set and there's an actual channel active.
		if any(self.channel_active) and not self.__graphRefreshing:
			self.ToggleGraphRefreshing()


	def OnTBAutomaticUpdate(self,e):
		"""ToggleButton for enabling/disabling auto graph refreshing."""
		tb=e.GetEventObject()
		if self.__graphRefreshing != tb.GetValue() and any(self.channel_active):	# We want to enable graph refreshing
			self.ToggleGraphRefreshing()											# 	if channels are active, for sure.
	
	def OnStartAll(self,e):
		"""Starts all available not started channels."""
		e.GetEventObject().Disable()
		if(self.acqPanel0.Module and not self.channel_active[0] and self.channel_available[0]):
			self.acqPanel0.StartClick(e)
		if(self.acqPanel1.Module and not self.channel_active[1] and self.channel_available[1]):
			self.acqPanel1.StartClick(e)
		if(self.acqPanel2.Module and not self.channel_active[2] and self.channel_available[2]):
			self.acqPanel2.StartClick(e)
		if(self.acqPanel3.Module and not self.channel_active[3] and self.channel_available[3]):
			self.acqPanel3.StartClick(e)

	
	def OnStopAll(self,e):
		"""	Stops all active channels."""	
		if(self.acqPanel0.Module and self.channel_active[0]):
			self.acqPanel0.StopClick(e)
		if(self.acqPanel1.Module and self.channel_active[1]):
			self.acqPanel1.StopClick(e)
		if(self.acqPanel2.Module and self.channel_active[2]):
			self.acqPanel2.StopClick(e)
		if(self.acqPanel3.Module and self.channel_active[3]):
			self.acqPanel3.StopClick(e)

	def OnRefreshAll(self,e):
		"""	Pulls data from the modules and immediately prints it on the plot."""
		self.RefreshGraphOnce()

class Plot(wx.Panel):
	"""Graph panel"""
	def __init__(self, parent, id = -1, dpi = None, **kwargs):
	 	wx.Panel.__init__(self, parent, id=id, **kwargs)
		self.figure = mpl.figure.Figure(dpi=dpi, figsize=(2,2))
		self.canvas = Canvas(self, -1, self.figure)
		self.toolbar = Toolbar(self.canvas)
		self.toolbar.Realize()

		#Start all channels button
		self.BStartAll = wx.BitmapButton(self,-1,wx.Image("./graphics/start-button.png",wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		self.BStopAll = wx.BitmapButton(self,-1,wx.Image("./graphics/stop-button.png",wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		self.BRefreshAll = wx.BitmapButton(self,-1,wx.Image("./graphics/refresh-button.png",wx.BITMAP_TYPE_PNG).ConvertToBitmap())
		#Update frequency control
		self.TBGraphRefreshing =  wx.ToggleButton(self,label="Automatic Update",size=(-1,-1))
		self.TBGraphRefreshing.SetValue(True)
		self.sld_updFreq = wx.Slider(self, -1, parent.update_frequency, 1, 20, wx.DefaultPosition, (200, -1),wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_TOP | wx.SL_LABELS)

		canvasSizer = wx.BoxSizer(wx.HORIZONTAL)
		canvasSizer.Add(self.canvas,1,wx.EXPAND)

		sizer = wx.BoxSizer(wx.VERTICAL)
		toolbarSizer = wx.BoxSizer(wx.HORIZONTAL)
		toolbarSizer.Add(self.toolbar, 1 , wx.ALL | wx.EXPAND)
		toolbarSizer.Add(self.BRefreshAll,0,wx.ALL | wx.EXPAND, border=1)
		toolbarSizer.Add(self.BStopAll,0,wx.ALL | wx.EXPAND, border=1)
		toolbarSizer.Add(self.BStartAll,0,wx.ALL | wx.EXPAND, border=1)
		toolbarSizer.Add(self.TBGraphRefreshing,0,wx.ALL | wx.EXPAND, border=1)
		toolbarSizer.Add(self.sld_updFreq,0,wx.ALL | wx.EXPAND, border=1)
		sizer.Add(canvasSizer,1,wx.EXPAND)
		sizer.Add(toolbarSizer,0,wx.EXPAND)
		self.SetSizer(sizer)
