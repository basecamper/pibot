import json

from Log import log

from Message.Message import Message
from Message import TYPES
from Message import TARGETS
from Message.PhoneParser import PhoneParser

from codecs import decode
from codecs import encode


class Factory:
	
	@staticmethod
	def objectFromArray(array):
		#log("Factory.fromClient(): %s" % array)
		if len(array) % 2 != 0:
			raise ValueError("Factory.objectFromArray(array): uneven array")
		obj = {}
		
		for c in range(0,len(array),2):
			obj[array[c]] = array[c+1] or ""
		
		return obj
	
	
	@staticmethod
	def fromClient(text:str, sourceSocket) -> Message:
		try:
			#log("Factory.fromClient(): %s" % text)
			array = text.split(',')
			type = array[0]
			if type == "phone":
				return Message(
					type=TYPES.PHONE_REQUEST,
					source=TARGETS.CLIENT,
					destination=TARGETS.PHONE,
					sourceSocket=sourceSocket,
					data={"cmd":",".join(array[1:])})
			elif type == "phonelog":
				return Message(
					type=TYPES.PHONELOG,
					source=TARGETS.CLIENT,
					destination=TARGETS.SYSTEM,
					sourceSocket=sourceSocket)
			
		except Exception as e:
			log("MessageFactory: invalid client request, data: %s" % text)
			return Message(
				type=TYPES.PHONE_INVALID_REQUEST,
				source=TARGETS.BOT,
				destination=TARGETS.CLIENT,
				sourceSocket=sourceSocket,
				data={ "error" : "invalid request"}
			)
	
	@staticmethod
	def toPhone(message:Message) -> bytes:
		return encode(u"AT%s\n" % message.data["cmd"], "latin_1")
	
	@staticmethod
	def fromPhone(data:bytes) -> Message:
		return PhoneParser.parse(data)
	
	@staticmethod
	def toClient(message:Message) -> str:
		data = message.data or {}
		str = json.dumps(data)
		return str