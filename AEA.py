from managerServer import serverInit
from managerHardware import Lights, Mister, Fan, Peltier
from os import walk, path
import json

if __name__ == '__main__':
    try:
        # start server
        HOST_NAME = 'localhost'
        PORT_NUMBER = 8000
        serverInit(HOST_NAME, PORT_NUMBER)

        # init lights
        lights = Lights("RELAY1")
        lights.startscheduledlighting()

        # init mister
        mister = Mister("RELAY2")
        mister.startscheduledmisting()

        # init fan
        fan = Fan("RELAY3")
        fan.startscheduledfanning()

        # init peltier
        peltier = Peltier("RELAY4")
    
    # try and switch things switch off if there are any errors or user shutdown
    except:
        try:
            lights.off()
        except:
            pass

        try:
            mister.off()
        except:
            pass

        try:
            fan.off()
        except:
            pass

        try:
            peltier.off()
        except:
            pass



        