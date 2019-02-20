import time

from Message.Message import Message
from Message import TARGETS


def redirectToSource(message:Message):
	
	src, dest, srcS, destS = message.source,\
							 message.destination,\
							 message.destinationSocket,\
							 message.sourceSocket
	
		
	message.destination = dest
	message.source = src
	message.sourceSocket = srcS
	message.destinationSocket = destS

def msTimestamp():
	return int(round(time.time() * 1000))