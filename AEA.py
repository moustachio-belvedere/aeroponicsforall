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
        lights.inrangestart()
        lights.startscheduledlighting()

        # init mister
        mister = Mister("RELAY2")

    
    # try and switch things switch off if there are any errors or user shutdown
    except:
        try:
            lights.lightsoff()
        except:
            pass

        try:
            mister.misteroff()
        except:
            pass


        