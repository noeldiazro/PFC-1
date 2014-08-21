# coding=utf-8
# CSV READER
import csv
import numpy
import classes.Points as Points
import csv, codecs, cStringIO

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

class Writer:
	"""
		A CSV writer which will write rows to CSV file "f",
		which is encoded in the given encoding.
		Source: https://docs.python.org/2/library/csv.html
		Modified by Diego Muñoz to accept a filepath instead of a filestream
	"""

	def __init__(self, filepath, dialect=csv.excel, encoding="utf-8", **kwds):
		# Redirect output to a queue
		self.queue = cStringIO.StringIO()
		self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
		self.stream = open(filepath, 'wb')
		self.encoder = codecs.getincrementalencoder(encoding)()

	def writerow(self, row):
		self.writer.writerow([str(s).encode("utf-8") for s in row])
		# Fetch UTF-8 output from the queue ...
		data = self.queue.getvalue()
		data = data.decode("utf-8")
		# ... and reencode it into the target encoding
		data = self.encoder.encode(data)
		# write to the target stream
		self.stream.write(data)
		# empty queue
		self.queue.truncate(0)

	def writerows(self, rows):
		for row in rows:
			self.writerow(row)
		
