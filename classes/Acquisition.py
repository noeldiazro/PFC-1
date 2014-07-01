import time
from math import sin, pi, floor
class Acquisition:
    '''This class represents an acquisition object'''

    def __init__(self, sampling_rate=1):
        self.__sampling_rate = sampling_rate
        self.__sampling_period = 1.0/sampling_rate
        self.__data = []
        self.__status = 'waiting'

    def set_sampling_rate(self, sampling_rate):
        self.__sampling_rate = sampling_rate
        self.__sampling_period = 1.0/sampling_rate

    def get_sampling_rate(self):
        return self.__sampling_rate

    def start(self):
        self.__status = 'running'
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            adc_value = floor(4096*(0.5*(sin(2*pi*elapsed_time)+1)))
            self.__data.append([elapsed_time, adc_value])
            print(elapsed_time, adc_value)
            time.sleep(self.__sampling_period)

    def stop(self):
        self.__status = 'stopped'

    def get_data(self):
        return self.__data

    def get_status(self):
        return self.__status
