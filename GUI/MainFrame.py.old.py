#!/usr/bin/python
# -*- coding: utf-8 -*-

# Used to guarantee to use at least Wx2.8
import wxversion
wxversion.ensureMinimal('2.8')

import os
import wx
import wx.aui
import matplotlib as mpl
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar


class MainFrame(wx.Frame):
	def __init__(self, parent, title):
		self.dirname=''

		# A "-1" in the size parameter instructs wxWidgets to use the default size.
		# In this case, we select 200px width and the default height.
		#wx.Frame.__init__(self, parent, title=title, size=(-1,-1))
		super(MainFrame, self).__init__(parent, title=title, size=(-1, -1))
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


		# Sizers
		sizer = wx.BoxSizer(wx.VERTICAL)
		upperSizer = wx.BoxSizer(wx.VERTICAL)
		lowerSizer = wx.BoxSizer(wx.HORIZONTAL)
		leftSizer = wx.BoxSizer(wx.HORIZONTAL)


		self.nb = wx.aui.AuiNotebook(self)
		upperSizer.Add(self.nb,1,wx.EXPAND)

		lowerSizer.Add(wx.Button(self,label="Abajo"),1,wx.BOTTOM)
		leftSizer.Add(wx.Button(self,label="Izquierda"),1,wx.BOTTOM)

		# EXAMPLE PLOT
		page = Plot(self.nb)
		self.nb.AddPage(page,"plot")
		axes1 = page.figure.gca()
		axes1.plot([1,2,3],[2,1,4])
		#

		# Sizer addings
		#self.sizer.Add(self.upperSizer,2,wx.TOP)
		sizer.Add(lowerSizer,1,wx.BOTTOM)
		#self.sizer.Add(self.leftSizer,1,wx.LEFT)
		self.SetMinSize(self.GetSize())


		# Events.
		self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

		
		self.Show()

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