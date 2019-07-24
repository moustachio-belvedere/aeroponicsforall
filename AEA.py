from managerHardware import Lights, Mister, Fan, Peltier
from threading import Thread
from os import walk, path
from time import sleep, asctime
from http.server import HTTPServer
from backendServer import Server
import json

if __name__ == '__main__':
    try:
        # init lights
        lights = Lights("RELAY1")
        lights.startscheduledlighting()

        # init mister
        mister = Mister("RELAY2")
        mister.startscheduledmisting(everyNsec = 10, forNsec = 5)

        # init fan
        fan = Fan("RELAY3")
        fan.startscheduledfanning(everyNsec = 10, forNsec = 5)

        # init peltier
        peltier = Peltier("RELAY4")

        # start server
        HOST_NAME = 'localhost'
        PORT_NUMBER = 8000
        httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
        print(asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))
        httpd.serve_forever()

    # try and switch things switch off if there are any errors or user shutdown
    except KeyboardInterrupt:

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



        
