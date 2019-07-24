from backendRelay import Relay
from backendTimerUtils import RepeatedTimer, time_in_range
from threading import Lock, Thread
from time import sleep
import datetime
import schedule

class Lights(Relay):
    def __init__(self, relaystring):
        super(Lights, self).__init__(relaystring, "Lights")

    def inrangestart(self):
        ton_parsed = datetime.time(*self.ton)
        toff_parsed = datetime.time(*self.toff)

        timenow = datetime.datetime.now().time()

        if time_in_range(ton_parsed, toff_parsed, timenow):
            self.on()
        else:
            self.off()

    def timestringparse(self, pt):
        return "{}:{}".format(str(pt[0]).zfill(2), str(pt[0]).zfill(2))

    def scheduledlighting(self):
        with self.schedulerlock:
            ton_parsed = timestringparse(self.ton)
            toff_parsed = timestringparse(self.toff)

            lightschedule = schedule.Scheduler()

            lightschedule.every().day.at(ton_parsed).do(self.on)
            lightschedule.every().day.at(toff_parsed).do(self.off)

            while 1:
                lightschedule.run_pending()
                time.sleep(1)

    def startscheduledlighting(self, ton = (8, 0), toff = (22, 0)):
        self.ton = ton
        self.toff = toff

        self.inrangestart()

        self.schedulerthread = Thread(target = self.scheduledmisting, name="Lighting Scheduler Thread")
        self.schedulerlock = Lock()

        self.schedulerthread.start()

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
                time.sleep(1)

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
                time.sleep(1)

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

