import sys
import traceback
import fcntl
import os
import time
from  datetime import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Log:

    enabled = True
    entryExit = True


    indent = 1
    def __init__(self):
        f = sys._getframe(1)

        filename = f.f_code.co_filename
        className = ''

        if 'self' in f.f_locals:
            className = f.f_locals['self'].__class__.__name__

        funcName = f.f_code.co_name

        self.funcName=funcName
        self.className=className
        self.timeEnter = time.time()

        if(Log.enabled and Log.entryExit):
            print timeStamp(),
            print " " * Log.indent,
            print bcolors.HEADER + "Enter %s.%s()" % (self.className,self.funcName) + bcolors.ENDC
        Log.indent = Log.indent +4

    def __del__(self):
        Log.indent=Log.indent-4
        if(Log.enabled and Log.entryExit):
            print timeStamp(), int((time.time()-self.timeEnter)*1000),
            print " " * Log.indent,
            print bcolors.HEADER +  "Exit %s.%s()" % (self.className,self.funcName) + bcolors.ENDC

    def logDebug(self,logItem):
        if(Log.enabled):
            print timeStamp(),
            print " " * Log.indent,
            print bcolors.OKBLUE + (logItem) + bcolors.ENDC

    def logInfo(self,logItem):
        if(Log.enabled):
            print timeStamp(),
            print " " * Log.indent,
            print bcolors.OKGREEN + (logItem) + bcolors.ENDC
'''
def timeStamp(showDate = True, showTime = True, showMsec = True):
    t = time.time()
    fmt1 = "%y-%m-%d" if showDate else ""
    fmt2 = "%H:%M:%S" if showTime else ""
    fmt = " ".join((fmt1, fmt2))
    s = time.strftime(fmt, time.localtime(t))
    if showMsec:
        msec = "%.3f" % (t%1.0)
        s += msec[1:]
    return s
'''

def timeStamp():
    t = time.time()
    return  datetime.utcfromtimestamp(t)

def logException(e):
    exFmt = "-" * 80
    exFmt += "\nTime: " 
    exFmt += str(timeStamp())
    exFmt += "\n"
    exFmt += traceback.format_exc()
    exFmt += "\n"
    with open("exception.log", "a") as exFd:
        fcntl.lockf(exFd, fcntl.LOCK_EX)
        exFd.seek(os.SEEK_END, 0)
        exFd.write(exFmt)
        fcntl.lockf(exFd, fcntl.LOCK_UN)
    print(exFmt)


