from Message.Message import Message

from Message import TYPES, TARGETS

from Log import logRead
from Log import log
class System:
	
	@staticmethod
	def answer(message:Message):
		if message.type == TYPES.PHONELOG:
			return Message(
				type=TYPES.ANSWER,
				source=TARGETS.BOT,
				destination=TARGETS.CLIENT,
				destinationSocket=message.sourceSocket,
				data={"phone.log":logRead()}
			)