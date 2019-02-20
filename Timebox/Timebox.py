#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from Timebox.TimeboxLL import TimeboxLL
from Timebox.RainbowColors import RainbowColors
from Log import log

import time

'''VIEWTYPES = {
	"clock": 0x00,
	"temp": 0x01,
	"off": 0x02,
	"anim": 0x03,
	"graph": 0x04,
	"image": 0x05,
	"stopwatch": 0x06,
	"scoreboard": 0x07
}'''


SERVICE_UUIDS = [
	"49535343-fe7d-4ae5-8fa9-9fafd205e455",
	"49535343-8841-43f4-a8d4-ecbe34729bb3",
	"00002902-0000-1000-8000-00805f9b34fb",
	"49535343-1e4d-4bd9-ba61-23c647249616",
	"00002902-0000-1000-8000-00805f9b34fb",
	"49535343-aca3-481c-91ec-d85e28a60318",
	"00002902-0000-1000-8000-00805f9b34fb",
	"49535343-6daa-4d02-abf6-19569aca69fe",
	"0000180a-0000-1000-8000-00805f9b34fb",
	"00002a2a-0000-1000-8000-00805f9b34fb",
	"00002a23-0000-1000-8000-00805f9b34fb",
	"00002a28-0000-1000-8000-00805f9b34fb",
	"00002a26-0000-1000-8000-00805f9b34fb",
	"00002a27-0000-1000-8000-00805f9b34fb",
	"00002a25-0000-1000-8000-00805f9b34fb",
	"00002a24-0000-1000-8000-00805f9b34fb",
	"00002a29-0000-1000-8000-00805f9b34fb"
]

class Timebox(TimeboxLL):
	
	def switchView(self, type):
		log("Timebox.switchView() %s" % (type))
		if not self.working:
			self.working = True
			self._send( self._switch_view(type) )
		
		else:
			log("Timebox: working..")
	
	def rainbowClock(self):
		if not self.working:
			self.working = True
			r, g, b, self._rainbowCounter = RainbowColors.get(self._rainbowCounter)
			
			self.setTimeColor( r, g, b )
			self.working = False
		else:
			log("Timebox: working..")
	def randomClockColor(self):
		if not self.working:
			self.working = True
			self.setTimeColor( random.randint(0,8), random.randint(0,8), random.randint(0,8) )
			self.working = False
		else:
			log("Timebox: working..")
	def setTimeColor(self, r, g, b, x=0x00):
		if not self.working:
			self.working = True
			self._send( self._set_time_color(r, g, b, x) )
			self.working = False
		else:
			log("Timebox: working..")
	
	def volume(self, level):
		if not self.working:
			self.working = True
			self._send( self._volume(level) )
			self.working = False
		else:
			log("Timebox: working..")
	
	def printServices(self):
		for uuid in SERVICE_UUIDS:
			self._print_service(uuid)
	
	def __init__(self, addr):
		super().__init__(addr)
		self._rainbowCounter = 0
		self._connect()
		self.working = False
