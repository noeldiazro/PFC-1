# coding=utf-8
# CSV READER
import csv
import numpy
import classes.Points as Points

class Reader:

	def __init__(self, filename=None):
		#print "Abriendo fichero..."
		self.file=filename
		#print self.file
		with open(self.file, 'rU') as csvfile:
			spamreader = csv.reader(csvfile,  delimiter='\t')
			self.strTitle = spamreader.next()[0].decode('mac-roman')
			tmp = spamreader.next()
			self.strXLabel = tmp[0].decode('mac-roman')
			self.strYLabel = tmp[1].decode('mac-roman')

			self.p=Points.Points()	#Storage for the points read from file.

			#print "Creando Puntos..."
			for row in spamreader:
				self.p.append(float(row[0]),float(row[1]))
			
			"""
			print "Calculando máximos y mínimos..."
			self.xMax = numpy.amax(self.p.x)
			self.xMin = numpy.amin(self.p.x)
			self.yMax = numpy.amax(self.p.y)
			self.yMin = numpy.amin(self.p.y)
			"""

			#Limpiamos memoria
			del tmp

			#print "Terminado. Elementos: "+str(self.p.length())

