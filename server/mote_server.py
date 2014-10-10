from pymongo import MongoClient
from datetime import datetime
import serial


class MoteServer:
	def __init__(self, moteCount):
		self.functions = list()
		self.datastore = dict()
		self.moteCount = moteCount

	def mongoInit(self):
		self.db_client = MongoClient("localhost")
		self.db = self.db_client.mote
		self.data_collection = self.db.data

	def register(self, func):
		if not callable(func):
			raise Exception("Not a function")
		self.functions.append((func.__name__, func))

	def listFunc(self):
		for name, func in self.functions:
			print name

	def getFuncNames(self):
		return tuple([name[0] for name in self.functions])

	def isFunc(self, name):
		return name in self.getFuncNames()

	def call(self, func_name, args):
		for name, func in self.functions:
			if name==func_name:
				print func(*args)
				break	

	def retrieve(self, key):
		try:
			val = self.datastore[key]
			print "retrieved: "+val
			return val
		except:
			return "INVALID"

	def store(self, key, val):
		print "stored: "+val
		self.datastore[key] = val
	
	def handle(self, msg):
		splitted = msg.split("/")
		firstPar = splitted.pop(0)
		if self.isFunc(firstPar): self.call(firstPar, splitted)
		elif len(splitted) == 1: self.store(firstPar, splitted[0])
		elif len(splitted) == 0: self.retrieve(firstPar)
		else: raise Exception("Cannot handle the message")
			
	def poll(self):
		pass

def F1(a,b):
	return "F1"+a+b
def F2(a,b):
	return "F2"+str(int(a)+int(b))
def F3(a,b):
	return "F3"

if __name__ == "__main__":
	s = MoteServer(5)
	s.register(F1)
	s.register(F2)
	s.register(F3)
	s.listFunctions()
	for i in range(10):
		str_i = str(i)
		s.store(str_i+"/"+str_i)
