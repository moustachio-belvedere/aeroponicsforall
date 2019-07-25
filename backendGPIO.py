import RPi.GPIO as GPIO

class GPIOManager:
	def __init__(self):
		# init pin naming convention and warnings
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		
		# init I2C power pin and switch on
		print("Initialising I2C Power...")
		self.I2Cpowerpin = 40
		GPIO.setup(self.I2Cpowerpin, GPIO.OUT)
		GPIO.output(self.I2Cpowerpin, GPIO.HIGH)
		print("I2C Power ON.")
		
	def initGPIO(self, pin):
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.LOW)

	def onGPIO(self, pin):
		GPIO.output(pin, GPIO.HIGH)
		
	def offGPIO(self, pin):
		GPIO.output(pin, GPIO.LOW)
		
	def powerdown(self):
		GPIO.output(self.I2Cpowerpin, GPIO.LOW)
		print("I2C Power OFF.")
		#~ GPIO.cleanup()
		print("GPIO Cleanup Complete.")



