from pymongo import MongoClient
from datetime import datetime
from time import sleep
import zmq
import bus

class MoteServer:
    def __init__(self, moteList):
        bus.Init()
        bus.FetchHandle = self.FetchHandle
        bus.StoreHandle = self.StoreHandle
        self.functions = list()
        self.datastore = dict()
        self.moteList = moteList
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:5006")

    def MongoInit(self):
        self.db_client = MongoClient("192.168.0.191")
        self.db = self.db_client.mote
        self.data_collection = self.db.data

    def Register(self, func):
        if not callable(func):
            raise Exception("Not a function")
        self.functions.append((func.__name__, func))

    def ListFunc(self):
        for name, func in self.functions:
            print name

    def GetFuncNames(self):
        return tuple([name[0] for name in self.functions])

    def IsFunc(self, name):
        return name in self.GetFuncNames()

    def Call(self, func_name, args=None):
        func_name = str(func_name)
        for name, func in self.functions:
            if name==func_name:
                if args==None:
                    print func()
                else:
                    print args
                    print func(args)

    def Retrieve(self, key):
        try:
            val = self.datastore[key]
            print "retrieved: "+val
            return val
        except:
            return "INVALID"

    def Persist(self, key, val):
        print "stored: "+val
        self.datastore[key] = val
    
    def Handle(self, msg):
        splitted = msg.split("/")
        firstPar = splitted.pop(0)
        if self.isFunc(firstPar): self.Call(firstPar, splitted)
        elif len(splitted) == 1: self.Persist(firstPar, splitted[0])
        elif len(splitted) == 0: self.Retrieve(firstPar)
        else: raise Exception("Cannot handle the message")

    def StoreHandle(self, recv):
        cmd = recv[5:]
        print cmd
        splitted = cmd.split("/")
        firstPar = splitted.pop(0)
        print splitted, firstPar
        if self.IsFunc(firstPar): self.Call(firstPar, splitted[0])
        elif len(splitted) == 1: self.Persist(firstPar, splitted[0])
        else: raise Exception("Cannot handle the message")

    def FetchHandle(self, dst, recv):
        pass
    
    def ProcessCommands(self):
        try:
            msg = self.socket.recv(zmq.NOBLOCK)
        except:
            pass
        else:
            dst = msg[0]
            cmd = msg[1]
            topic = msg[2:]
            if cmd == "@":
                resp = bus.Fetch(dst, topic)
                self.socket.send(resp[5:])
                print "Fetch:"+topic+"="+resp
            elif cmd == "!":
                bus.Store(dst, topic)
                self.socket.send("")
                print "Store:"+topic
            
    def Run(self):
        from itertools import cycle
        for mote in cycle(self.moteList):
            self.ProcessCommands()   
            sleep(0.5)
            bus.Poll(mote)
            sleep(0.5)

def SMS(msg):
    import sms
    sms.SendSMStelus(msg)

def F2(a,b):
    return "F2"+str(int(a)+int(b))
def F3(a,b):
    return "F3"

if __name__ == "__main__":
    s = MoteServer(["B"])
    s.Register(SMS)
    s.Register(F2)
    s.Register(F3)
    s.ListFunc()
    #for i in range(10):
    #    str_i = str(i)
    #    s.Persist(str_i,str_i)
    s.Run()
