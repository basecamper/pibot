from Message.Message import Message

from tornado.queues import LifoQueue

class BotQueue():
	
	queue = LifoQueue()
	
	@staticmethod
	async def asyncPut(message:Message):
		await BotQueue.queue.put(message)
	
	@staticmethod
	def put(message:Message):
		BotQueue.queue.put(message)
	
	@staticmethod
	async def consumer(dispatchFunc):
		while True:
			async for message in BotQueue.queue:
				try:
					await dispatchFunc(message)
				finally:
					BotQueue.queue.task_done()