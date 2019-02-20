from tornado.websocket import WebSocketHandler

from BotQueue import BotQueue

from Message.Factory import Factory

from Log import log
from Message.Message import Message

sockets = []

class WebSocket(WebSocketHandler):
	
	def open(self):
		log("Websocket Opened")
		sockets.append(self)
	
	async def on_message(self, text):
		log("Websocket message: %s" % text)
		
		request = Factory.fromClient(text, self)
		if request:
			await BotQueue.asyncPut(request)
	
	def on_close(self):
		log("Websocket closed")
		sockets.remove(self)
	
	def check_origin(self, origin):
		log("Websocket check_origin %s" % origin)
		return True
	
	