from managerHardware import Lights, Mister, Fan, Peltier
from threading import Thread
from os import walk, path
from time import sleep, asctime
from http.server import HTTPServer
from backendServer import Server
from backendGPIO import GPIOManager
from backendI2C import Sensors
from backendCamera import Camera
import json

if __name__ == '__main__':
    try:
        # init GPIO
        gpiomanager = GPIOManager()
        
        # init camera to take picture every 5 seconds
        camera = Camera(5)
        camera.start_timed_capture()

        # init lights
        lights = Lights("RELAY1", gpiomanager, camera)
        lights.startscheduledlighting(ton = (8, 0), toff = (22, 0))

        #~ # init mister
        #~ mister = Mister("RELAY2", gpiomanager)
        #~ mister.startscheduledmisting(everyNsec = 10, forNsec = 5)

        #~ # init fan
        #~ fan = Fan("RELAY3", gpiomanager)
        #~ fan.startscheduledfanning(everyNsec = 10, forNsec = 5)

        #~ # init peltier
        #~ peltier = Peltier("RELAY4", gpiomanager)
        
        #~ # init sensors
        #~ sensors = Sensors()
        #~ sensors.startsensorpoll()
        #~ sensors.startfilewriterthread()

        # start server
        HOST_NAME = 'localhost'
        PORT_NUMBER = 8000
        httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
        print(asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))
        httpd.serve_forever()

    # try and switch things switch off if there are any errors or user shutdown
    except KeyboardInterrupt:
        try:
            camera.stop_timed_capture()
        except BaseException as e:
            print("\n\Camera off may have failed due to error:\n{}\n".format(e))

        try:
            lights.lightschedule.sentinel = False
            lights.lightschedule.stop()
            lights.lightschedulethread.join()
            lights.off()
        except BaseException as e:
            print("\n\nLights off may have failed due to error:\n{}\n".format(e))

        try:
            mister.misterschedule.sentinel = False
            mister.misterschedule.stop()
            mister.misterschedulethread.join()
            mister.off()
        except BaseException as e:
            print("\n\nMister off may have failed due to error:\n{}\n".format(e))

        try:
            fan.fanschedule.sentinel = False
            fan.fanschedule.stop()
            fan.fanschedulethread.join()
            fan.off()
        except BaseException as e:
            print("\n\Fan off may have failed due to error:\n{}\n".format(e))

        try:
            peltier.off()
        except BaseException as e:
            print("\n\Peltier off may have failed due to error:\n{}\n".format(e))

        try:
            httpd.server_close()
            print(asctime(), 'Server DOWN - %s:%s' % (HOST_NAME, PORT_NUMBER))
        except:
            pass
            
        try:
            sensors.sentinel = False
            sensors.filewriterthreadtimer.stop()
            #~ sensors.lightschedulethread.join()
        except BaseException as e:
            print("\n\Sensors off may have failed due to error:\n{}\n".format(e))

        try:
            gpiomanager.powerdown()
        except BaseException as e: 
            print("\n\GPIO powerdown may have failed due to error:\n{}\n".format(e))
