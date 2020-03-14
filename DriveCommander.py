from DataSender  import DataSender
import threading


class DriveCommander(threading.Thread):
    sender = DataSender("ServerDriver")
    ReadyToStop = False

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):

        while not self.ReadyToStop:
            cmd = input ("Select command: fw, bw, tr, tl, ar, al")
            switch = {"fw": self.GetFwParameters, "bw": self.GetFwParameters, "tr": self.GetRotateParameters, "tl": self.GetRotateParameters, "ar": self.GetArcParameters, "al": self.GetArcParameters}
            payload = switch[cmd](cmd)
            self.sender.SendToServer('robot/driver',payload)

    def Stop(self):
        self.ReadyToStop = True

    def GetFwParameters(self, cmd):
        speed = input("Speed[mm/s]:")
        distance = input("Distance[mm]:")
        return {"command" : cmd, "speed" : speed, "distance" : distance}

    def GetRotateParameters(self, cmd):
        angulspeed = input("Angular Speed [deg/s]")
        angle = input ("angle [deg]")
        return {"command" : cmd, "anglspeed" : angulspeed, "angle" : angle}

    def GetArcParameters(self, cmd):
        return