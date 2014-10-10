from itertools import cycle
import mote_server
import random
import time
import sys

class ServerSim(mote_server.MoteServer):
	def Run(self):
		for address in cycle(self.moteList):
			print "Accessing mote "+address
			try:
				msg = mList[index].msg.pop()
			except:
				msg = ""
				print "No more message for mote "+str(index)
			else:
				self.Handle(msg)
			print ""
			time.sleep(0.5)

class Mote:
	def __init__(self, msg):
		self.msg = msg 

#Functions to register
def getYear():
	return time.gmtime().tm_year

def getPercent():
	return random.randint(0,100)

def getPlatform():
	return sys.platform

def getParam(par1):
	return str(par1)

def addParam(par1, par2):
	return str(int(par1)+int(par2))

m1 = Mote(["getYear","addParam/75/25","data1/fred"])
m2 = Mote(["getPercent","getPlatform","getPercent"])
m3 = Mote(["data1","getPlatform","getYear"])
m4 = Mote(["getParam/hey","getPercent"])
m5 = Mote(["getParam/testing","addParam/80/8","addParam/13/17"])
mList = [m1, m2, m3, m4, m5]

s = ServerSim(["A","B"])
s.Register(getYear)
s.Register(getPercent)
s.Register(getPlatform)
s.Register(getParam)
s.Register(addParam)

print "This is a list of registered functions on server"
s.ListFunc()
print ""
s.Run()
