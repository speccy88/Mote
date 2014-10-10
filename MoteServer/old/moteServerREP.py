from pymongo import MongoClient
from datetime import datetime
from time import sleep
import thread
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
        self.commands = {}
        self.CommandServer(self.commands)

    def MongoInit(self):
        self.db_client = MongoClient("localhost")
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
        return name in self.getFuncNames()

    def Call(self, func_name, args):
        for name, func in self.functions:
            if name==func_name:
                print func(*args)
                break   

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
        elif len(splitted) == 1: self.Persis(firstPar, splitted[0])
        elif len(splitted) == 0: self.Retrieve(firstPar)
        else: raise Exception("Cannot handle the message")

    @staticmethod
    def StoreHandle(recv):
        pass

    @staticmethod
    def FetchHandle(dst, recv):
        pass
    
    def CommandServer(self, commands):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5006")
        def Listener(socket, commands):
            while(True):
                command = socket.recv()
                commands[command] = True
                socket.send(command)
        thread.start_new_thread(Listener,(socket, commands))
            
    def Run(self):
        from itertools import cycle
        for mote in cycle(self.moteList):
            for key in self.commands:
                if self.commands[key]:
                    self.commands[key] = False
                    bus.Store(mote, key)
               
            bus.Poll(mote)
            sleep(1)

def F1(a,b):
    return "F1"+a+b
def F2(a,b):
    return "F2"+str(int(a)+int(b))
def F3(a,b):
    return "F3"

if __name__ == "__main__":
    s = MoteServer(["B"])
    s.Register(F1)
    s.Register(F2)
    s.Register(F3)
    s.ListFunc()
    for i in range(10):
        str_i = str(i)
        s.Persist(str_i,str_i)
    s.Run()
