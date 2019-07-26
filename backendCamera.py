from datetime import datetime
from picamera import PiCamera
from pathlib import Path
from threading import Lock, Thread
from backendTimerUtils import IndefiniteTimer
from backendJSONUtil import appendtoJSON
from time import sleep

class Camera(PiCamera):
	
	def __init__(self, everyN):
		super(Camera, self).__init__()
		
		# set up camera hardware variables
		self.initvar_camerahardware()
		
		# every N seconds take picture
		self.everyN = everyN
		
		# lock to activate whilst still port in use
		self.piclock = Lock()
		
		# camera sentinel to only take pictures when light is on
		self.sentinel = False
		
	def initvar_camerahardware(self):
		# set default resolution
		self.resolution = (640, 480)
		
		# turn off de-noiser for still and video images
		self.image_denoise = True
		self.video_denoise = False
		
		# ensure saturation turned off
		#~ self.saturation = 0
		
		# auto-white balance, starts auto
		self.awb_mode = 'auto'
		
	def capture(self):
		with self.piclock:
			if self.sentinel:
				filename = '{timestamp:%Y%m%d}_{timestamp:%H%M%S}.jpg'.format(timestamp=datetime.now())
				impath = 'public/images_lores/' + filename
				
				print("taken picture at:", "{timestamp:%H-%M-%S}".format(timestamp=datetime.now())) 
				
				# use parent method to capture, *bayer and quality only used for JPG formats*
				super(Camera, self).capture(impath, format='jpeg', use_video_port=False, bayer=False, quality=60)
				
				appendtoJSON('public/images_lores/listofimages.json', filename)
			
	def start_timed_capture(self):
		# init timed camera capture 
		self.cameratimer = IndefiniteTimer(self.everyN, self.capture)
		self.cameratimerthread = Thread(target = self.cameratimer.start_all)
		self.cameratimerthread.start()	
		
	def stop_timed_capture(self):
		try:
			self.cameratimer.stop()
		except AttributeError:
			pass
