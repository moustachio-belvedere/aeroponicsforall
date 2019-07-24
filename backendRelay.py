# !/usr/bin/python

# Library for PiRelay
# Developed by: SB Components
# Author: Ankur
# Project: PiRelay
# Python: 3.4.2

#===========================================================================
# import RPi.GPIO as GPIO
# import time

# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)

# class Relay:
#     ''' Class to handle Relay
#     Arguments:
#     relay = string Relay label (i.e. "RELAY1","RELAY2","RELAY3","RELAY4")
#     '''
#     relaypins = {"RELAY1":15, "RELAY2":13, "RELAY3":11, "RELAY4":7}

    # def __init__(self, relay, device):
    #     self.pin = self.relaypins[relay]
    #     self.relay = relay
    #     GPIO.setup(self.pin, GPIO.OUT)
    #     GPIO.output(self.pin, GPIO.LOW)
    #     self.device = device
    #     print("{} device initialised on {}.".format(self.device, self.relay))

    # def on(self):
    #     GPIO.output(self.pin, GPIO.HIGH)
    #     self.ison = True
    #     print("{} connected to {} - ON".format(self.device, self.relay))

    # def off(self):
    #     GPIO.output(self.pin, GPIO.LOW)
    #     self.ison = False
    #     print("{} connected to {} - OFF".format(self.device, self.relay))
#===========================================================================

class Relay:
    # dummy class for testing purposes
    relaypins = {"RELAY1":15, "RELAY2":13, "RELAY3":11, "RELAY4":7}

    def __init__(self, relay, device):
        self.pin = self.relaypins[relay]
        self.relay = relay
        self.device = device
        print("{} device initialised on {}.".format(self.device, self.relay))

    def on(self):
        self.ison = True
        print("{} on {} - ON".format(self.device, self.relay))

    def off(self):
        self.ison = False
        print("{} on {} - OFF".format(self.device, self.relay))
