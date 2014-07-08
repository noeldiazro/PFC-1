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



class MainFrame(wx.Frame):

	def __init__(self, parent, title):
		super(MainFrame, self).__init__(parent, title=title, 
			size=(-1, -1))
			
		self.InitUI()
		self.Centre()
		self.SetMinSize(self.GetSize())
		self.Maximize()
		self.Show()     
		
	def InitUI(self):
		self.dirname=''
		self.CreateStatusBar() # A Statusbar in the bottom of the window
		# Setting up the menu.
		fileMenu = wx.Menu()
		helpMenu = wx.Menu()
		menuOpen = fileMenu.Append(wx.ID_OPEN, "&Abrir"," Abrir una sesión")
		menuExit = fileMenu.Append(wx.ID_EXIT,"&Salir"," Salir del programa")

		menuHelp= helpMenu.Append(wx.ID_HELP, "&Ayuda"," Ayuda general")
		menuAbout= helpMenu.Append(wx.ID_ABOUT, "Acerca &de"," Acerca de este programa")

		# Creating the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu,"&Archivo") # Adding the "fileMenu" to the MenuBar
		menuBar.Append(helpMenu,"&A&yuda")
		self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.


		panel = wx.Panel(self)

		vbox = wx.BoxSizer(wx.VERTICAL)

		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)

		## hbox1
		# EXAMPLE PLOT
		page = Plot(panel)
		self.axes1 = page.figure.gca()
		#self.axes1.plot([1,2,3],[2,1,4])
		#
		

		## hbox2


		self.nb = wx.aui.AuiNotebook(panel,style=wx.aui.AUI_NB_TOP)

		# TEST PANELS
		acqPanel = GUI.AcquisitionGUI.AcquisitionGUI(self)

		self.nb.AddPage(acqPanel,"Adquisicion")
		self.nb.AddPage(wx.Panel(self),"Datos")
		self.nb.AddPage(wx.Panel(self),"Exportar")

		hbox1.Add(page, 1, flag=wx.EXPAND)
		hbox2.Add(self.nb,1, flag=wx.EXPAND)
		vbox.Add(hbox1, 2, flag=wx.EXPAND | wx.ALL)
		vbox.Add(hbox2, 1, flag=wx.EXPAND | wx.ALL)

		

		panel.SetSizer(vbox)


		# Events.
		self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)


	def OnAbout(self,e):
		# Create a message dialog box
		dlg = wx.MessageDialog(self, "Proyecto de Final de Carrera \n Diego Muñoz Callejo", "Acerca de", wx.OK)
		dlg.ShowModal() # Shows it
		dlg.Destroy() # finally destroy it when finished.

	def OnExit(self,e):
		self.Close(True)  # Close the frame.

	def OnOpen(self,e):
		""" Open a file """
		dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			f = open(os.path.join(self.dirname, self.filename), 'r')

			f.close()
		dlg.Destroy()

class Plot(wx.Panel):
	def __init__(self, parent, id = -1, dpi = None, **kwargs):
		wx.Panel.__init__(self, parent, id=id, **kwargs)
		self.figure = mpl.figure.Figure(dpi=dpi, figsize=(2,2))
		self.canvas = Canvas(self, -1, self.figure)
		self.toolbar = Toolbar(self.canvas)
		self.toolbar.Realize()

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.canvas,1,wx.EXPAND)
		sizer.Add(self.toolbar, 0 , wx.LEFT | wx.EXPAND)
		self.SetSizer(sizer)