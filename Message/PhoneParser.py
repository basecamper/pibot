from codecs import decode
from codecs import encode
import re
from Phone.ResultParser import ResultParser as RP

from Log import log, logWrite

from Message.Message import Message

from Message import TYPES, TARGETS


class PhoneParser:



    @staticmethod
    def _splitValues(vdata):
        return vdata.replace('"','').split(',')

    @staticmethod
    def _tryParseUtf(text:str) -> str:
        temp = decode(text, "hex")
        return decode(temp, "utf-8")

    @staticmethod
    def _tryParseLatin(text:str) -> str:
        temp = decode(text, "hex")
        return decode(temp, "latin_1")

    @staticmethod
    def _tryParseText(text:str):
        log("PhoneParser._tryParseText(): text: %s " % text)

        temp = ""
        exception = True

        if exception:
            exception = False
            try:
                temp = PhoneParser._tryParseUtf(text)
                log("PhoneParser._tryParseUtf(): success: %s" % temp)
            except Exception as e:
                log("PhoneParser._tryParseUtf(): exception: %s" % e)
                exception = True

        if exception:
            exception = False
            try:
                temp = PhoneParser._tryParseLatin(text)
                log("PhoneParser._tryParseLatin(): success: %s" % temp)
            except Exception as e:
                log("PhoneParser._tryParseLatin(): exception: %s" % e)
                exception = True

        if exception:
            log("PhoneParser._tryParseText(): returning raw")
            temp = text
        return temp

    @staticmethod
    def _parseOperatorList(rawData:str) -> object:
        splitted = rawData.replace('(',"").split("),")
        operators = splitted[:-2]
        returnObj = {}
        c = 0
        op = 0
        for part in splitted:
            if c == 0:
                returnObj[op] = {}
                returnObj[op]["status"] = RP.parse("opStat", part)
            elif c == 1:
                returnObj[op]["long alphanumeric"] = RP.parse("string", part)
            elif c == 2:
                returnObj[op]["short alphanumeric"] = RP.parse("string", part)
            else:
                returnObj[op]["numeric"] = RP.parse("string", part)

            c+=1
            if c == 4:
                op += 1
                c = 0

        returnObj["supported modes"] = splitted[-2]
        returnObj["supported formats"] = splitted[-1].replace(")",'')

    @staticmethod
    def _parseData(text:str, message:Message):

        log (text)

        messageData = {}

        cmdPattern = re.compile(r"\+.+: ")
        errorPattern = re.compile(r"\+.+ERROR: ")
        cmdMatch = re.match(cmdPattern,text)
        cmdError = re.match(errorPattern,text)

        if cmdMatch:

            cmd = re.sub('[: ]','',cmdMatch.group(0))
            cmdSplit = re.split(cmdPattern, text)
            dataRaw = cmdSplit[1]
            data = re.split(r'[,]', dataRaw)

            print(data)


            if cmdError:
                message.data["ERROR"] = data[0]
            elif cmd == '+CRING':
                message.data["RING"] = RP.parse("string", data[0])
            elif cmd == '+CR':
                message.data["service report"] = RP.parse("string", data[0])
            elif cmd == '+COPS':
                message.data["operator selection"] = {}

                if "(" in data[0]:
                    message.data["operator selection"] = PhoneParser._parseOperatorList(dataRaw);

                else:
                    message.data["operator selection"]["mode"] = RP.parse("opMode", data[0])
                    if data.__len__() > 1:
                        message.data["operator selection"]["format"] = RP.parse("opFormat", data[1])
                        message.data["operator selection"]["operator"] = RP.parse("string", data[2])
            elif cmd == '+CPAS':
                message.data["activity"] = RP.parse("pas", data[0])
            elif cmd == '+CCLK':
                message.data["date"] = RP.parse("time", dataRaw)
            elif cmd == '+CSQ':
                message.data["signal"] = {}
                message.data["signal"]["rssi"] = RP.parse("rssi",data[0])
                message.data["signal"]["rxqual"] = RP.parse("ber",data[1])
            elif cmd == '+CBC':
                message.data["battery"] = {}
                message.data["battery"]["status"] = RP.parse("bcs",data[0])
                message.data["battery"]["remaining"] = RP.parse("bcl",data[1])
                message.data["battery"]["volt"] = RP.parse("voltage",data[2])
            elif cmd == '+CSCS':
                message.data["chset"] = RP.parse("string", dataRaw)
            elif cmd == '+CLIP':
                message.writeToLog = True
                message.data["clip"] = {}
                message.data["clip"]["number"] = RP.parse('number',data[0])
                message.data["clip"]["type"] = RP.parse('number',data[1])
                message.data["clip"]["subaddr"] = RP.parse('number',data[2])
                message.data["clip"]["satype"] = RP.parse('number',data[3])
                message.data["clip"]["entry"] = RP.parse('string',data[4])
                message.data["clip"]["validity"] = RP.parse('number',data[5])
            elif cmd == '+CMTI':
                message.writeToLog = True
                message.data["newSms"] = {}
                message.data["newSms"]["entry"] = RP.parse('string',data[0])
                message.data["newSms"]["num"] = RP.parse('number',data[1])
            elif cmd == '+CMGL':
                message.data["sms"] = {}
                message.data["sms"]["id"] = RP.parse('number',data[0])
                message.data["sms"]["status"] = RP.parse('smsStat',data[1])
                message.data["sms"]["sender"] = RP.parse('string',data[2])
                message.data["sms"]["entry"] = RP.parse('string',data[3])
                message.data["sms"]["date"] = RP.parse('time',data[4]+','+data[5])
                if 'REC' in data[1] and data.__len__() > 6:
                    message.data["sms"]["sender type"] = RP.parse('tooa', data[6])
                    message.data["sms"]["first octet"] = RP.parse('number', data[7])
                    message.data["sms"]["protocol"] = RP.parse('pid', data[8])
                    message.data["sms"]["data coding scheme"] = RP.parse('dcs', data[9])
                    message.data["sms"]["sc"] = RP.parse('string', data[10])
                    message.data["sms"]["sc type"] = RP.parse('string', data[11])
                    message.data["sms"]["length"] = RP.parse('string', data[12])
            elif cmd == '+CMGR':
                message.data["sms"] = {}
                message.data["sms"]["status"] = RP.parse('smsStat',data[0])
                message.data["sms"]["sender"] = RP.parse('string',data[1])
                message.data["sms"]["entry"] = RP.parse('string',data[2])
                message.data["sms"]["date"] = RP.parse('time',data[3]+','+data[4])
                if 'REC' in data[0] and data.__len__() > 5:
                    message.data["sms"]["sender type"] = RP.parse('tooa', data[5])
                    message.data["sms"]["first octet"] = RP.parse('number', data[6])
                    message.data["sms"]["protocol"] = RP.parse('pid', data[7])
                    message.data["sms"]["data coding scheme"] = RP.parse('dcs', data[8])
                    message.data["sms"]["sc"] = RP.parse('string', data[9])
                    message.data["sms"]["sc type"] = RP.parse('string', data[10])
                    message.data["sms"]["length"] = RP.parse('string', data[11])
            elif cmd == '+CREG':
                message.data["network registration"] = {}
                stat = ""
                lac = ""
                ci = ""
                if data.__len__() == 1:
                    message.data["network registration"]["status"] = RP.parse('regStat',data[0])
                elif data.__len__() == 4:
                    message.data["network registration"]["setting"] = RP.parse('string',data[0])
                    stat = RP.parse('regStat',data[1])
                    lac = "%s \"%s\"" % (RP.parse('string',data[2]), RP.parse('hex',data[2]))
                    ci = "%s \"%s\"" % (RP.parse('string',data[3]), RP.parse('hex',data[3]))

                else:
                    stat = RP.parse('regStat',data[0])
                    lac = "%s \"%s\"" % (RP.parse('string',data[1]),RP.parse('hex',data[1]))
                    ci = "%s \"%s\"" % (RP.parse('string',data[2]), RP.parse('hex',data[2]))

                message.data["network registration"]["status"] = stat
                message.data["network registration"]["location area code"] = lac
                message.data["network registration"]["cell id"] = ci
            elif cmd == '+CRLP':
                message.data["radio link protocol"] = {}
                message.data["radio link protocol"]["interworking window size"] = RP.parse('number',data[0])
                message.data["radio link protocol"]["mobile window size"] = RP.parse('number',data[1])
                message.data["radio link protocol"]["acknowledgement timer t1"] = RP.parse('T1',data[2])
                message.data["radio link protocol"]["retransmission attempts"] = RP.parse('number',data[3])
                message.data["radio link protocol"]["re-sequencing period"] = RP.parse('T4',data[4])
            else:
                if not cmd in message.data:
                    message.data[cmd] = {}

                c = 1
                if cmd in message.data:
                    while "%d"%c in message.data[cmd]:
                        c+=1
                    print ("%d"%c)
                message.data[cmd]["%d"%c] = dataRaw

        else:
            if text == 'RING':
                message.writeToLog = True
                message.type = TYPES.PHONE_DATA_RING

            elif text == 'NO CARRIER':
                message.type = TYPES.PHONE_DATA_NO_CARRIER

            elif text == 'OK':
                message.type = TYPES.PHONE_ANSWER_OK

            elif text == 'ERROR':
                message.type = TYPES.PHONE_ANSWER_ERROR
                message.data["status"] = "ERROR"
            else:
                message.data["text"] = PhoneParser._tryParseText(text)

    @staticmethod
    def sanitizeData(data:bytes) -> str:
        outstr = ""
        try:
            outstr = decode( data, "UTF-8" )
        except Exception as e:
            try:
                outstr = decode( data, "latin-1" )
            except Exception as e2:
                logWrite("Phoneparser.sanitizeData: Exception2: data: %s" % data)
                outstr =  data.decode()
        finally:
            return outstr

    @staticmethod
    def parse(data:bytes) -> Message:
        message = Message(type=TYPES.PHONE_DATA_UNKNOWN,
                          source=TARGETS.PHONE,
                          destination=TARGETS.BOT,
                          data={})
        dataArray = data.split(b'\r\n')

        for part in dataArray:
            if len(part):
                PhoneParser._parseData(PhoneParser.sanitizeData(part), message)

        #log("PhoneParser.parse(): returning: %s" % message)
        return message