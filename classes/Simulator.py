# coding=utf-8
from utils import CSVUtils
import clock
import time
import threading
import classes.Points as Points

class Simulator:
	def __init__(self, sampling_rate=1):
		self.sampling_rate = sampling_rate
		self.status = "No Input"
		self.stopAcq = False
		self._data = Points.Points()
		self.start_time_lock = threading.Lock()
		self.start_time_lock.acquire()
		self.LOCK = threading.Lock()

	#Given Python nature this isn't very useful
	def set_sampling_rate(new_sampling_rate):
		self.sampling_rate=new_sampling_rate
	#Or this
	def get_sampling_rate():
		return self.sampling_rate

	def start(self):
		if(self.csv):
			print "Acquiring Started"
			self._start_time = clock.time()
			self.start_time_lock.release()
			self.stopAcq = False
			self.status="running"
			t = threading.Thread(target=self.startAcquiring)
			t.daemon=True
			t.start()


	def stop(self):
		self.stopAcq=True
		print "Acquiring Stopped"
		self.status="stopped" #This should be a paused status, but we have to fix a lot of things already.

	def get_data(self, n_count=0):
		p = []
		# Data is an iterated Point list, so we have to iterate n_counts
		p.append(self._data.getLast())
		for i in range(-n_count-1,self._data.length()):
			p.append(self._data.next())
		return p

	data = property(get_data)

	# Start Time
	@property
	def start_time(self):
		return self._start_time
	def get_status(self):
		return self.status

	"""
		CSV SPECIFIC FUNCTIONS
	"""
	def setFileInput(self,filePath):
		self.csv = CSVUtils.Reader(filePath)
		#print self.csv.strTitle

	def startAcquiring(self):
		#print "delay:"+str(1.0/self.sampling_rate)
		while(not self.stopAcq):
			try:
				tmp=self.csv.p.next()
				with self.LOCK:
					self._data.append(tmp[0],tmp[1])
				time.sleep(1.0/self.sampling_rate)
			except StopIteration:
				#start over
				pass
				
