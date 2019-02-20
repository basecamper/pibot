import time
import codecs

from Message.Message import Message

logfile = "./phone.log"

def log(message:str):
    print(message)
    return True

def logMessage(message:Message):
    logWrite("%s: %s" % (message.type, message.data))

def logWrite(message:str):
    def writeLog(m):
        with codecs.open(logfile, "a", encoding="utf-8") as file:
            file.write(m)
    lm = u"%s   %s" % (time.ctime(), message)
    writeLog(lm+'\n')

def logRead() -> str:
    data = ""
    try:
        f = open(logfile,'r')
        data = f.read()
        f.close()
    except:
        data="Could not open logfile."
    return data