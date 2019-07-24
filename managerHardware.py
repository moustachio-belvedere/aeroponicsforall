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
        print("Light function ran at {}".format(timenow))
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

        # every sixty seconds, check if in desired time window for lights on
        self.lightschedule = IndefiniteTimer(2, self.inrangeON)
        self.lightschedulethread = Thread(target = self.lightschedule.start_all)
        self.lightschedulethread.start()

class Mister(Relay):
    def __init__(self, relaystring):
        super(Mister, self).__init__(relaystring, "Mister")

    def onemistingcycle(self):
        self.on()
        sleep(self.forNsec)
        self.off()

    def scheduledmisting(self):
        with self.schedulerlock:
            mistingschedule = schedule.Scheduler()
            mistingschedule.every(self.everyNmin).minutes.do(self.onemistingcycle)

            while 1:
                mistingschedule.run_pending()
                sleep(1)

    def startscheduledmisting(self, everyNmin = 1, forNsec = 25):
        assert type(everyNmin)==int, "Must be a whole integer number of minutes."
        assert type(forNsec)==int, "Must be a whole integer number of seconds."
        assert everyNmin*60 >= forNsec, "Time misting must be less than time between misting cycles."

        self.everyNmin = everyNmin
        self.forNsec = forNsec

        self.schedulerthread = Thread(target = self.scheduledmisting, name="Misting Duty Cycle Thread")
        self.schedulerlock = Lock()

        self.schedulerthread.start()

class Fan(Relay):
    def __init__(self, relaystring):
        super(Fan, self).__init__(relaystring, "Fan")

    def onefancycle(self):
        self.on()
        sleep(self.forNsec)
        self.off()

    def scheduledfan(self):
        with self.schedulerlock:
            fanschedule = schedule.Scheduler()
            fanschedule.every(self.everyNmin).minutes.do(self.onefancycle)

            while 1:
                fanschedule.run_pending()
                sleep(1)

    def startscheduledfanning(self, everyNmin = 1, forNsec = 45):
        assert type(everyNmin)==int, "Must be a whole integer number of minutes."
        assert type(forNsec)==int, "Must be a whole integer number of seconds."
        assert everyNmin*60 >= forNsec, "Time fanning must be less than time between fan cycles."

        self.everyNmin = everyNmin
        self.forNsec = forNsec

        self.schedulerthread = Thread(target = self.scheduledfan, name="Fan Duty Cycle Thread")
        self.schedulerlock = Lock()

        self.schedulerthread.start()

class Peltier(Relay):
    def __init__(self, relaystring):
        super(Peltier, self).__init__(relaystring, "Peltier")

