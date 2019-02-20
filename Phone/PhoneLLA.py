import asyncio

from BotQueue import BotQueue
from Message.Factory import Factory


class PhoneLLA(asyncio.Protocol):
	
	''' warning +CPMS echoes with storage sizes & a separate OK'''
	cfgcmd = 'E0Q0S0=0S3=13V1X4;+IFC=0,0;+IPR=115200;'+\
	'+CMGF=1;+CSCS="8859-1";+CPMS="MT","ME","ME";'+ \
	'+CLIP=1;+VTD=50;+DDET=1,0,0;'+ \
	'&W'
	'''+CMEE=2 # verbose cme errors'''
	'''+CR=1 # call setup service report'''
	'''+CRC=1 # +CRING instead of RING'''
	connection = None
	buffer = bytes(1024)
	
	def connection_made(self, transport):
		PhoneLLA.connection = self
		self.transport = transport
		print('PhoneLLA port opened', transport)
	
	def data_received(self, data):
		#print('PhoneLLA data received', data)
		PhoneLLA.buffer += data
		self.reviewBuffer()
		
	def reviewBuffer(self):
		if PhoneLLA.buffer[-2:] == b'\r\n':
			BotQueue.put(Factory.fromPhone(PhoneLLA.buffer))
			PhoneLLA.buffer = b''
	
	def connection_lost(self, exc):
		print('PhoneLLA port closed')
		PhoneLLA.connection = None
		self.transport.close()