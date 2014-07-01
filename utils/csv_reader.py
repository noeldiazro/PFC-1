# coding=utf-8
# CSV READER
import csv
import numpy

class csv_reader:

	def __init__(self, filename=None):
		print "Abriendo fichero..."
		self.file=filename
		print self.file
		with open(self.file, 'rU') as csvfile:
			spamreader = csv.reader(csvfile,  delimiter='\t')
			self.strTitle = spamreader.next()[0].decode('mac-roman')
			tmp = spamreader.next()
			self.strXLabel = tmp[0].decode('mac-roman')
			self.strYLabel = tmp[1].decode('mac-roman')

			self.puntos = []
			x = []	# temporales para calcular
			y = []	#  máximos y mínimos

			print "Creando Puntos..."
			for row in spamreader:
				self.puntos.append([[float(row[0])],[float(row[1])]])
				x.append(float(row[0]))
				y.append(float(row[1]))

			print "Calculando máximos y mínimos..."
			self.xMax = numpy.amax(x)
			self.xMin = numpy.amin(x)
			self.yMax = numpy.amax(y)
			self.yMin = numpy.amin(y)

			#Limpiamos memoria
			del x
			del y
			del tmp

			print "Terminado. Elementos: "+str(len(self.puntos))