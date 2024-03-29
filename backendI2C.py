from time import sleep
from smbus2 import SMBusWrapper
from bitstring import Bits
from threading import Thread, Lock
from backendTimerUtils import IndefiniteTimer
from backendJSONUtil import appendtoJSON
from datetime import datetime

class Sensors:
	def __init__(self, peltier):
		self.addressT74 = 0x4d # temp sensor address
		self.addressHON = 0x27 # honeywell address
		
		self.HONtemp = 0.0
		self.HONrelh = 0.0
		self.T74temp = 0.0
		
		self.peltier = peltier
		
	def __getstatus(self, h1s):
		h1sB = format(h1s, '08b')
		status = h1sB[:2]
		return status

	def __HONparsetemp(self, t1, t2):
		t1real = format(t1, '08b')
		t2parse = format(t2, '08b')
		t2real = t2parse[:len(t2parse)-2]
		
		fulltbin = t1real + t2real
		
		fullt = int(fulltbin, 2)
		
		self.HONtemp = (fullt/(2**14 - 2))*165 - 40
		
	def __HONparsehumid(self, h1s, h2):
		h1parse = format(h1s, '08b')
		h1real = h1parse[2:] 
		h2real = format(h2, '08b')
		
		fullhbin = h1real + h2real
		
		fullh = int(fullhbin, 2)
		
		self.HONrelh = (fullh/(2**14 - 2))*100
		
	def sensorpoll(self):
		with SMBusWrapper(1) as bus:
			while self.sentinel:
				readT74, = bus.read_i2c_block_data(self.addressT74, 0, 1)
				tempbits = format(readT74, '08b')
				tempBit = Bits(bin=tempbits)
				self.T74temp = tempBit.int - 1 # correction for wrong voltage supplied
				
				read1 = bus.read_i2c_block_data(self.addressHON, 0, 4)
				hum1stat, hum2, temp1, temp2 = read1
				
				self.__HONparsetemp(temp1,temp2)
				self.__HONparsehumid(hum1stat,hum2)
				
				sleep(0.1)

	def startsensorpoll(self):
		self.sentinel = True
		pollthread = Thread(target=self.sensorpoll)
		pollthread.start()
		
	def filewritetarget(self):
		with self.filewritelock:
			appendtoJSON('public/sensordata/datim.json', '{timestamp:%Y-%m-%d} {timestamp:%H:%M:%S}'.format(timestamp=datetime.now()))
			appendtoJSON('public/sensordata/tempT74.json', self.T74temp)
			appendtoJSON('public/sensordata/tempHON.json', self.HONtemp)
			appendtoJSON('public/sensordata/relhHON.json', self.HONrelh)
		
		self.peltier.updatefromtemp(self.T74temp)
		
		print("\nTemp T74: {}\nTemp HON: {}\nHumi HON: {}\n".format(self.T74temp, self.HONtemp, self.HONrelh)) 
		
	def startfilewriterthread(self, secondsPerWrite = 5):
		self.filewritelock = Lock()
		self.filewriterthreadtimer = IndefiniteTimer(secondsPerWrite, self.filewritetarget)
		self.filewriterthreadtimer.start_all()
		
if __name__=="__main__":
	sensors = Sensors()
	sensors.startsensorpoll()
	sensors.startfilewriterthread()
