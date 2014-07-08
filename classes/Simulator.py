# coding=utf-8
from utils import csv_reader
import time
from threading import Thread

class Simulator:
	def __init__(self, sampling_rate=1):
		self.sampling_rate = sampling_rate
		self.status = "No Input"
		self.stopAcq = False
		self.data = []

	#Given Python nature this isn't very useful
	def set_sampling_rate(new_sampling_rate):
		self.sampling_rate=new_sampling_rate
	#Or this
	def get_sampling_rate():
		return self.sampling_rate

	def start(self):
		if(self.csv):
			print "Acquiring Started"
			self.stopAcq = False
			self.status="Running"
			t = Thread(target=self.startAcquiring)
			t.start()


	def stop(self):
		self.stopAcq=True
		print "Acquiring Stopped"
		self.status="Stopped"

	#or this
	def get_data():
		pass
	#and this
	def get_status():
		pass

	"""
		CSV SPECIFIC FUNCTIONS
	"""
	def setFileInput(self,filePath):
		self.csv = csv_reader.csv_reader(filePath)
		print self.csv.strTitle

	def startAcquiring(self):
		iterator = iter(self.csv.puntos)
		print "delay:"+str(1.0/self.sampling_rate)
		while(not self.stopAcq):
			try:
				self.data.append(iterator.next())
				#print time.ctime()
				time.sleep(1.0/self.sampling_rate)
			except StopIteration:
				self.stop() 
				return
