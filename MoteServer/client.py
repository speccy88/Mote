import zmq

class MoteClient:
    def __init__(self, serverAddress):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://"+serverAddress+":5006")

    def Close(self):
        self.socket.close()
        self.context.term()

    def Fetch(self, addr, msg):
        self.SendMSG(addr,"@"+msg)
        return self.GetMSG()
        
    def Store(self, addr, msg):
        self.SendMSG(addr,"!"+msg)
        self.GetMSG()

    def SendMSG(self, addr, msg):
        self.socket.send(addr+msg)
    
    def GetMSG(self):
        return self.socket.recv()

    def Ask(self):
        while(True):
            print ""
            print """\
(1)Store = LED/ON
(2)Store = LED/OFF
(3)Store next poll = TIME
(4)Store = MAIL
(5)Fetch = COUNTER """
            choice = raw_input("?")
            if choice == "0":
                self.Store(ADDRESS,"")
            elif choice == "1":
                self.Store(ADDRESS,"LED/ON")
            elif choice == "2":
                self.Store(ADDRESS,"LED/OFF")
            elif choice == "3":
                self.Store(ADDRESS,"TIME")
            elif choice == "4":
                self.Store(ADDRESS,"MAIL")
            elif choice == "5":
                print self.Fetch(ADDRESS,"COUNTER")
            else:
                self.Close()
                quit()

if __name__=="__main__":
    c = MoteClient("192.168.0.198")
    ADDRESS = "B"
    c.Ask()
