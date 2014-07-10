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

			#self.puntos = []
			self.x = []	# temporales para calcular
			self.y = []	#  máximos y mínimos

			print "Creando Puntos..."
			for row in spamreader:
				# matplotlib won't use this kind of list, so commented until further notice.
				#self.puntos.append([float(row[0]),float(row[1])])	
				# x and y lists will be used instead.
				self.x.append(float(row[0]))
				self.y.append(float(row[1]))
			
			print "Calculando máximos y mínimos..."
			self.xMax = numpy.amax(self.x)
			self.xMin = numpy.amin(self.x)
			self.yMax = numpy.amax(self.y)
			self.yMin = numpy.amin(self.y)
			
			#Limpiamos memoria
			#del x
			#del y
			del tmp

			print "Terminado. Elementos: "+str(len(self.x))