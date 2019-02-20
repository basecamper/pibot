import re
from codecs import decode
from codecs import encode
class ResultParser:
	@staticmethod
	def _tryParseLatin(text:str) -> str:
		temp = decode(text, "hex")
		return decode(temp, "latin_1")
	@staticmethod
	def parse(type, v):
		#log("ResultParser.parse(): type: %s v: %s" % (type, v))
		if 'number' in type:
			return v
		
		elif 'string' == type:
			
			if re.match(r'^".*"$', v):
				return v[1:-1]
			
			return v
		
		elif 'type' == type or "tooa" == type:
			if '129' in v:
				return 'unknown'
			elif '161' in v:
				return 'national'
			elif '145' in v:
				return 'international'
			elif '177' in v:
				return 'network specific'
		
		elif 'subaddr' == type:
			return v
		
		elif 'satype' == type:
			return v
		
		elif 'CLI validity' == type:
			if '0' in v:
				return 'valid'
			elif '1' in v:
				return 'withheld'
			elif '2' in v:
				return 'error'
		
		elif 'pas' == type:
			if '0' in v:
				return 'ready'
			elif '2' in v:
				return 'unknown'
			elif '3' in v:
				return 'ringing'
			elif '4' in v:
				return 'call in progress'
		
		elif 'rssi' == type:
			iv = int(v)
			if iv == 0:
				return '-114'
			elif iv == 1:
				return '-111'
			elif iv > 1 and iv < 31:
				return "-"+str(110-(2*(int(v) -2)) )
			elif iv == 31:
				return '-52'
			elif iv == 99:
				return 'Unknown'
		
		elif 'ber' == type:
			if v == '99':
				return 'Unknown'
			return v
		
		elif 'bcs' == type:
			if v == '0':
				return 'not charging'
			if v == '1':
				return 'charging'
			if v == '2':
				return 'charging finished'
		
		elif 'bcl' == type:
			return v
		
		elif 'voltage' == type:
			return v
		
		elif 'time' == type:
			
			sv = v.replace('"','').split(',')
			date = sv[0].split('/')
			time = sv[1].split(':')
			time[2] = time[2].split('+')[0]
			
			return "%s.%s.%s %s:%s:%s".replace('"','') %\
				   ( date[0],date[1],date[2], time[0],time[1],time[2], )
		
		# +CMGL
		elif 'index' == type:
			return v
		
		elif 'stat' == type:
			return v
		
		elif 'pid' == type:
			if v == '0':
				return 'default'
			else:
				return v
		
		elif 'dcs' == type:
			if v == '0':
				return 'default'
			else:
				return v
		
		elif 'smsStat' == type:
			s = ResultParser.parse('string',v)
			if s == 'REC UNREAD':
				return 'recieved, unread'
			if s == 'REC READ':
				return 'recieved, read'
			if s == 'STO UNSENT':
				return 'stored, unsent'
			if s == 'STO SENT':
				return 'stored, sent'
			if s == 'ALL':
				return 'all'
		
		elif 'hex' == type:
			s = ResultParser.parse('string',v)
			print(s)
			return decode(decode(s,"hex"), "latin_1")
		
		
		elif 'regStat' == type:
			if v == '0':
				return 'not registered'
			if v == '1':
				return 'registered, home'
			if v == '2':
				return 'not registered, searching'
			if v == '3':
				return 'registration denied'
			if v == '4':
				return 'unknown'
			if v == '5':
				return 'registered, roaming'
		
		elif 'T1' == type:
			return "%dms" % (int(v)*10)
		
		elif 'T4' == type:
			return "%dms" % (int(v)*10)
		
		elif 'opMode' == type:
			if v == "0":
				return "auto"
			elif v == "1":
				return "manual"
			elif v == "2":
				return "deregistered"
			elif v == "3":
				return "set-only"
			elif v == "4":
				return "manual/Auto"
		
		elif 'opStat' == type:
			if v == "0":
				return "unknown"
			elif v == "1":
				return "available"
			elif v == "2":
				return "current"
			elif v == "3":
				return "forbidden"
		
		elif 'opFormat' == type:
			if v == "0":
				return "long format alphanumeric"
			elif v == "1":
				return "short format alphanumeric"
			elif v == "2":
				return "numeric (GSM Location Area Identification)"