#!/usr/bin/python
# -*- coding: utf-8 -*-

# border.py

import os
import wx
import wx.aui
import matplotlib as mpl
import GUI.AcquisitionGUI
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
from threading import Thread
import time




class MainFrame(wx.Frame):

	def __init__(self, parent, title):
		super(MainFrame, self).__init__(parent, title=title, 
			size=(-1, -1))
			
		#Variables used by the graph control
		self.update_frequency = 5
		self.autoscale = True
		self.channel_active = [False,False,False,False]
		self.__graphRefreshing=False


		self.InitUI()
		self.Centre()
		self.SetMinSize(self.GetSize())
		self.Maximize()
		self.Show()
		
	def InitUI(self):
		self.dirname=''
		self.statusbar=self.CreateStatusBar() # A Statusbar in the bottom of the window
		# Setting up the menu.
		fileMenu = wx.Menu()
		viewMenu = wx.Menu()
		helpMenu = wx.Menu()
		menuOpen = fileMenu.Append(wx.ID_OPEN, "&Abrir"," Abrir una sesión")
		menuExit = fileMenu.Append(wx.ID_EXIT,"&Salir"," Salir del programa")
		
		#View menu structure partially DISABLED
		vm_updateFreqSM = wx.Menu()
		"""
		vm_ufsm_fast = vm_updateFreqSM.Append(1, "Rápida (2s)",kind=wx.ITEM_RADIO)
		vm_ufsm_normal = vm_updateFreqSM.Append(2, "Normal (5s)",kind=wx.ITEM_RADIO).Check()
		vm_ufsm_slow = vm_updateFreqSM.Append(3, "Lenta (10s)",kind=wx.ITEM_RADIO)
		vm_ufsm_off = vm_updateFreqSM.Append(4, "Desactivar",kind=wx.ITEM_RADIO)
		vm_updateFreqSM.AppendSeparator()
		"""
		vm_ufsm_autos = vm_updateFreqSM.Append(5, "Autoescalado",kind=wx.ITEM_CHECK).Check()
		
		viewMenu.AppendSubMenu(vm_updateFreqSM,"Frecuencia de actualización")

		menuHelp= helpMenu.Append(wx.ID_HELP, "&Ayuda"," Ayuda general")
		menuAbout= helpMenu.Append(wx.ID_ABOUT, "Acerca &de"," Acerca de este programa")

		# Creating the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu,"&Archivo") # Adding the "fileMenu" to the MenuBar
		menuBar.Append(viewMenu,"&Ver")
		menuBar.Append(helpMenu,"&A&yuda")
		self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.



		vbox = wx.BoxSizer(wx.VERTICAL)

		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)

		## hbox1
		# EXAMPLE PLOT
		self.page = Plot(self)
		self.axes1 = self.page.figure.gca()
		#
		

		## hbox2


		self.nb = wx.aui.AuiNotebook(self,style=wx.aui.AUI_NB_TOP)

		# TEST PANELS
		self.acquisitionPage = wx.Panel(self)
		apshbox = wx.BoxSizer(wx.HORIZONTAL)


		self.acqPanel0 = GUI.AcquisitionGUI.AcquisitionGUI(self.acquisitionPage,self,0)
		self.acqPanel1 = GUI.AcquisitionGUI.AcquisitionGUI(self.acquisitionPage,self,1)
		self.acqPanel2 = GUI.AcquisitionGUI.AcquisitionGUI(self.acquisitionPage,self,2)
		self.acqPanel3 = GUI.AcquisitionGUI.AcquisitionGUI(self.acquisitionPage,self,3)
		apshbox.Add(self.acqPanel0,1,flag=wx.EXPAND)
		apshbox.Add(self.acqPanel1,1,flag=wx.EXPAND)
		apshbox.Add(self.acqPanel2,1,flag=wx.EXPAND)
		apshbox.Add(self.acqPanel3,1,flag=wx.EXPAND)
		self.acquisitionPage.SetSizer(apshbox)

		self.nb.AddPage(self.acquisitionPage,"Adquisicion")
		self.nb.AddPage(wx.Panel(self),"Datos")
		self.nb.AddPage(wx.Panel(self),"Exportar")

		hbox1.Add(self.page, 1, flag=wx.EXPAND)
		hbox2.Add(self.nb,1, flag=wx.EXPAND)
		vbox.Add(hbox1, 2, flag=wx.EXPAND | wx.ALL)
		vbox.Add(hbox2, 1, flag=wx.EXPAND | wx.ALL)

		

		self.SetSizer(vbox)


		# Events.
		self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		"""
		self.Bind(wx.EVT_MENU, self.SetUpdateFrequency,vm_ufsm_fast)
		self.Bind(wx.EVT_MENU, self.SetUpdateFrequency,vm_ufsm_normal)
		self.Bind(wx.EVT_MENU, self.SetUpdateFrequency,vm_ufsm_slow)
		self.Bind(wx.EVT_MENU, self.SetUpdateFrequency,vm_ufsm_off)
		"""
		self.Bind(wx.EVT_MENU, self.SetUpdateFrequency,vm_ufsm_autos)
		
		self.Bind(wx.EVT_SLIDER,self.SetUpdateFrequency,self.page.sld_updFreq)
		self.Bind(wx.EVT_TOGGLEBUTTON,self.OnTBAutomaticUpdate,self.page.TBGraphRefreshing)

	"""
		Graph refreshing. 
	"""
	def ToggleGraphRefreshing(self,check_channels=False):
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
		while (self.__graphRefreshing):
			# Pushes data for each channel if active:
			if(self.channel_active[0]):
				self.acqPanel0.PushData();
			if(self.channel_active[1]):
				self.acqPanel1.PushData();
			if(self.channel_active[2]):
				self.acqPanel2.PushData();
			if(self.channel_active[3]):
				self.acqPanel3.PushData();
			wx.CallAfter(self.__RefreshGraphLoop)
			if self.autoscale:
				self.axes1.autoscale()
			if (self.update_frequency>0):
				time.sleep(self.update_frequency)

	def __RefreshGraphLoop(self):
		self.page.canvas.draw()



	#							#
	#	E	V	E	N	T	S	#
	#							#
		

	def OnAbout(self,e):
		# Create a message dialog box
		dlg = wx.MessageDialog(self, "Proyecto de Final de Carrera \n Diego Muñoz Callejo", "Acerca de", wx.OK)
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

	"""
		ToggleButton for enabling/disabling auto graph refreshing.
	"""
	def OnTBAutomaticUpdate(self,e):
		tb=e.GetEventObject()
		if self.__graphRefreshing != tb.GetValue() and any(self.channel_active):	# We want to enable graph refreshing
			self.ToggleGraphRefreshing()											# 	if channels are active, for sure.

class Plot(wx.Panel):
	def __init__(self, parent, id = -1, dpi = None, **kwargs):
		wx.Panel.__init__(self, parent, id=id, **kwargs)
		self.figure = mpl.figure.Figure(dpi=dpi, figsize=(2,2))
		self.canvas = Canvas(self, -1, self.figure)
		self.toolbar = Toolbar(self.canvas)
		self.toolbar.Realize()

		#Update frequency control
		self.TBGraphRefreshing =  wx.ToggleButton(self,label="Automatic Update",size=(-1,-1))
		self.TBGraphRefreshing.SetValue(True)
		self.sld_updFreq = wx.Slider(self, -1, parent.update_frequency, 2, 20, wx.DefaultPosition, (200, -1),wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_TOP | wx.SL_LABELS)

		sizer = wx.BoxSizer(wx.VERTICAL)
		toolbarSizer = wx.BoxSizer(wx.HORIZONTAL)
		toolbarSizer.Add(self.toolbar, 1 , wx.LEFT | wx.EXPAND)
		toolbarSizer.Add(self.TBGraphRefreshing,0,wx.RIGHT | wx.EXPAND)
		toolbarSizer.Add(self.sld_updFreq,0,wx.RIGHT | wx.EXPAND)
		sizer.Add(self.canvas,1,wx.EXPAND)
		sizer.Add(toolbarSizer,0,wx.EXPAND)
		self.SetSizer(sizer)
