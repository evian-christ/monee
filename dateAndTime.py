import datetime
import time

today = datetime.datetime.now().strftime("%d-%m-%Y")

def strToUnix(s):
    return time.mktime(datetime.datetime.strptime(s, "%d-%m-%Y").timetuple())

def unixToStr(u):
    return datetime.datetime.fromtimestamp(u).strftime("%d-%m-%Y")