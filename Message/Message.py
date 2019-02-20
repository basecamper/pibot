from Message import TYPES
from Message import TARGETS


class Message:
	def __init__(self,
				 type:TYPES,
				 source:TARGETS,
				 destination:TARGETS,
				 sourceSocket = None,
				 destinationSocket = None,
				 data = None):
		
		#log("Message init")
		self.type = type
		self.source = source
		self.destination = destination
		
		self.sourceSocket = sourceSocket
		self.destinationSocket = destinationSocket
		
		self.data = data
		
		self.answer = None
		
		self.fullyProcessed = False
		
		self.writeToLog = False
	
	def __str__(self):
		answer = ' '
		sourceSocket = ' '
		if self.answer:
			answer += "--> %s" % self.answer
		datalen = 0
		if self.data:
			datalen = len(self.data)
		
		return "[ TYPE: %s SRC: %s DST: %s Datalen:%d %s ]%s"\
			   % (self.type, self.source, self.destination, datalen, self.data, answer)
	
	
	
	@classmethod
	def fromPhoneData(cls, data):
		cls()