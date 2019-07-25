import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)
pin = 21

#~ GPIO.setmode(GPIO.BOARD)
#~ GPIO.setwarnings(True)
#~ pin = 40

GPIO.setup(pin, GPIO.OUT)

GPIO.output(pin, GPIO.LOW)

GPIO.output(pin, GPIO.HIGH)
print("GPIO PIN ON")

time.sleep(15)

GPIO.output(pin, GPIO.LOW)
print("GPIO PIN OFF")

GPIO.cleanup()


