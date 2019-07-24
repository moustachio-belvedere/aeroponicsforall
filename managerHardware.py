from backendRelay import Relay
from backendTimerUtils import RepeatedTimer, time_in_range
from threading import Lock, Thread
import datetime
import schedule

class Lights:
    def __init__(self, relaystring, ton = (8, 0), toff = (22, 0)):
        self.lights = Relay(relaystring, "Lights")

        self.ton = ton
        self.toff = toff

    def inrangestart(self):
        ton_parsed = datetime.time(*self.ton)
        toff_parsed = datetime.time(*self.toff)

        timenow = datetime.datetime.now().time()

        if time_in_range(ton_parsed, toff_parsed, timenow):
            self.lightson()
        else:
            self.lightsoff()

    def timestringparse(self, pt):
        return "{}:{}".format(str(pt[0]).zfill(2), str(pt[0]).zfill(2))

    def lightson(self):
        self.lights.on()

    def lightsoff(self):
        self.lights.off()

    def scheduledlighting(self):
        with self.schedulerlock:
            ton_parsed = timestringparse(self.ton)
            toff_parsed = timestringparse(self.toff)

            lightschedule = schedule.Scheduler()

            lightschedule.every().day.at(ton_parsed).do(self.lightson())
            lightschedule.every().day.at(toff_parsed).do(self.lightsoff())

            while 1:
                lightschedule.run_pending()
                time.sleep(1)

    def startscheduledlighting(self):
        self.schedulerthread = Thread(target = self.scheduledmisting, name="Lighting Scheduler Thread")
        self.schedulerlock = Lock()

        self.schedulerthread.start()

class Mister:
    def __init__(self, relaystring, everyNsec = 60, forNsec = 25):
        self.mister = Relay(relaystring, "Mister")

        self.everyNsec = everyNsec
        self.forNsec = forNsec

    def misteron(self):
        self.mister.on()

    def misteroff(self):
        self.mister.off()

    def mistingdutycycle(self):
        with self.schedulerlock:


    def startsmistingdutycycle(self):
        self.mistingrepeater = RepeatedTimer()
        self.mistingthread = Thread(target = self.mistingdutycycle, name="Misting Duty Cycle Thread")
        self.mistinglock = Lock()

        self.schedulerthread.start()

    def mistingdutycycle(self):


    def scheduledmisting(self):
        with self.schedulerlock:
            ton_parsed = timestringparse(self.ton)
            toff_parsed = timestringparse(self.toff)

            lightschedule = schedule.Scheduler()

            lightschedule.every().day.at(ton_parsed).do(self.lightson())
            lightschedule.every().day.at(toff_parsed).do(self.lightsoff())

            while 1:
                lightschedule.run_pending()
                time.sleep(1)

    def startscheduledmisting(self):
        self.schedulerthread = Thread(target = self.scheduledmisting, name="Misting Duty Cycle Thread")
        self.schedulerlock = Lock()

        self.schedulerthread.start()

class Fan:
    def __init__(self):
        self.fan = Relay("RELAY3", "Fan")

class Peltier:
    def __init__(self):
        self.peltier = Relay("RELAY4", "Peltier")   
