#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import serial
import serial_asyncio
import tornado

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.web import Application, url

from Log import log, logMessage

from Message import TARGETS, TYPES
from Message.Factory import Factory
from Message.Message import Message

from Phone.PhoneLLA import PhoneLLA
from System.System import System
from Timebox.Timebox import Timebox

from WebSocket import WebSocket
from WebSocket import sockets

from Tools import msTimestamp

from BotQueue import BotQueue

class Bot():
    
    instance = None
    
    def __init__(self):
        
        log("Bot __init__")

        # self.timebox = Timebox('11:75:58:25:05:41');

        self.app = Application([url(r"/", WebSocket)])
        
        ##        Websocket port
        ##
        self.app.listen(12390)
        
        self.msHeartbeat = 1000
        ##        self.heartbeat sends the activity message
        ##        (and existing clients recieve the answer)
        
        self.activityMessage = Message(
            type=TYPES.PHONE_REQUEST,
            source=TARGETS.BOT,
            destination=TARGETS.PHONE,
            data={"cmd" : "+CPAS"})
        
        self.phoneRinging = False
        self.msTimestamp = 0
        
        IOLoop.current().spawn_callback(BotQueue.consumer, dispatchFunc=self._dispatch )
        
        IOLoop.current().spawn_callback(self.heartbeat)
        
        self.loop = tornado.ioloop.asyncio.get_event_loop()
        self.phoneCoroutine = serial_asyncio.create_serial_connection(
            self.loop,
            PhoneLLA,
            '/dev/serial0',
            baudrate=115200,
            timeout=5,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            rtscts=True)
        self.loop.run_until_complete(self.phoneCoroutine)
    
    
    
    async def heartbeat(self):
        while True:
            now = msTimestamp()
            old = self.msTimestamp
            self.msTimestamp = now
            #log("Bot.heartbeat(): %dms difference" % ((now - old) - self.msHeartbeat) )
            if PhoneLLA.connection:
                PhoneLLA.connection.transport.write( Factory.toPhone(self.activityMessage) )
            await gen.sleep(self.msHeartbeat/1000)
    
    async def _dispatch(self, message):
        
        if message.writeToLog:
            logMessage(message)
            log("Bot: logging message %s" % message)
            
        if message.destination == TARGETS.SYSTEM:
            message.sourceSocket.write_message( Factory.toClient( System.answer(message) ) )
        
        elif message.destination == TARGETS.CLIENT or message.destination == TARGETS.BOT:
            #log("Bot._dispatch() %s to %s " % (message, sockets))
            
            data = Factory.toClient(message)
            
            if message.destinationSocket:
                message.destinationSocket.write_message( data )
            else:
                print ("Writing to sockets: %s" % data.__str__())
                for socket in sockets:
                    socket.write_message( data )
        
        elif message.destination == TARGETS.PHONE:
            msg = Factory.toPhone(message)
            print ("Writing to phone: %s" % msg)
            PhoneLLA.connection.transport.write( msg)
        
        await gen.sleep(0.1)
    
    @staticmethod
    def run():
        if not Bot.instance:
            log("Bot: starting")
            Bot.instance = Bot()
            try:
                IOLoop.current().start()
            except:
                IOLoop.current().stop()

if __name__ == "__main__":
    Bot.run()
