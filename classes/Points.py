#!/usr/bin/python
# -*- coding: utf-8 -*-

class Points:

	def __init__(self,x=None,y=None):
		self.x = []
		self.y = []
		self.__i = 0
		if (x and y):
			self.x.append(x)
			self.y.append(y)
	
	def append(self,x,y):
		self.x.append(x)
		self.y.append(y)

	def length(self):
		return len(self.x)

	def resetIterator(self):
		self.__i = 0
	def next(self):
		self.__i += 1
		return [self.x[self.__i-1],self.y[self.__i-1]]

