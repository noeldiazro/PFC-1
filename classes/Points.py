#!/usr/bin/python
# -*- coding: utf-8 -*-

class Points:

	def __init__(self,x=None,y=None):
		self.x = []
		self.y = []
		self.__i = 0
		self.__offset = 0
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
		try:
			if self.__i<self.length():
				self.__i += 1
			else:
				self.__offset += self.x[self.__i-1]
				self.resetIterator()
				print "Iterator reset. New offset: ",self.__offset
				return [self.x[self.__i]+self.__offset,self.y[self.__i]]
			return [self.x[self.__i-1]+self.__offset,self.y[self.__i-1]]
		except IndexError  as e:
			print type(e)     # the exception instance
			print e.args      # arguments stored in .args
			print e           # __str__ allows args to printed directly