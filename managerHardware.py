from backendRelay import Relay
from backendTimerUtils import IndefiniteTimer, time_in_range
from threading import Thread
from time import sleep
import datetime

class Lights(Relay):
    def __init__(self, relaystring):
        super(Lights, self).__init__(relaystring, "Lights")

    def inrangeON(self):
        timenow = datetime.datetime.now().time()
        # print("Light function ran at {}".format(timenow))
        if time_in_range(self.ton, self.toff, timenow):
            if not self.ison:
                self.on()
        else:
            if self.ison:
                self.off()

    def timestringparse(self, pt):
        return "{}:{}".format(str(pt[0]).zfill(2), str(pt[0]).zfill(2))

    def startscheduledlighting(self, ton = (8, 0), toff = (22, 0)):
        self.ton = datetime.time(*ton)
        self.toff = datetime.time(*toff)

        # every ten seconds, check if in desired time window for lights on
        self.lightschedule = IndefiniteTimer(10, self.inrangeON)
        self.lightschedulethread = Thread(target = self.lightschedule.start_all)
        self.lightschedulethread.start()

class Mister(Relay):
    def __init__(self, relaystring):
        super(Mister, self).__init__(relaystring, "Mister")

    def onemistingcycle(self):
        self.on()
        for i in range(10*self.forNsec):
            if self.misterschedule.sentinel:
                sleep(0.1)
            else:
                break
        self.off()

    def startscheduledmisting(self, everyNsec = 60, forNsec = 25):
        assert everyNsec > forNsec, "Time misting must be less than time between misting cycles."

        self.everyNsec = everyNsec
        self.forNsec = forNsec

        # everyNsec mist forNsec
        self.misterschedule = IndefiniteTimer(self.everyNsec, self.onemistingcycle)
        self.misterschedulethread = Thread(target = self.misterschedule.start_all)
        self.misterschedulethread.start()

class Fan(Relay):
    def __init__(self, relaystring):
        super(Fan, self).__init__(relaystring, "Fan")

    def onefancycle(self):
        self.on()
        for i in range(10*self.forNsec):
            if self.fanschedule.sentinel:
                sleep(0.1)
            else:
                break
        self.off()

    def startscheduledfanning(self, everyNsec = 1, forNsec = 45):
        assert everyNsec > forNsec, "Time fanning must be less than time between fan cycles."

        self.everyNsec = everyNsec
        self.forNsec = forNsec

        # everyNsec fan forNsec
        self.fanschedule = IndefiniteTimer(self.everyNsec, self.onefancycle)
        self.fanschedulethread = Thread(target = self.fanschedule.start_all)
        self.fanschedulethread.start()

class Peltier(Relay):
    def __init__(self, relaystring):
        super(Peltier, self).__init__(relaystring, "Peltier")

