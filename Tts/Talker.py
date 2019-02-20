#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from subprocess import Popen
from gtts import gTTS
import os
class Talker:
	@staticmethod
	def getTimeDe() -> str:
		t = time.localtime()
		
		msg = u"Es ist %d uhr %d, und " % (t.tm_hour, t.tm_min)
		if ( t.tm_sec == 1 ):
			msg += u"eine sekunde."
		else:
			msg += u"%d sekunden." % t.tm_sec
		return msg
	@staticmethod
	def talk(text, filepath, lang):
		tts = gTTS(text=text, lang=lang)
		tts.save(filepath)

if __name__ == '__main__':
	filepathGood = "/home/pi/MissionControl_3_5/good.mp3"
	filepathBye = "/home/pi/MissionControl_3_5/bye.mp3"
	filepathDate = "/home/pi/MissionControl_3_5/date.mp3"
	filepathTheme = "/home/pi/MissionControl_3_5/theme.wav"
	
	#Talker.talk("Good night and good luck.",filepathBye,"en")
	#Talker.talk("Schönen guten tag!, ihr Anruf wurde gespeichert und sie können in kürze mit einem rückruf rechnen.",filepathGood)
	#Talker.talk(Talker.getTimeDe(),filepathDate, "de")
	
	a = Popen(["mplayer",filepathGood])
	b = Popen(["mplayer",filepathTheme])
	c = None
	while not time.sleep(0.1):
		if b.poll() == 0:
			c = Popen(["mplayer",filepathBye])
			break
	