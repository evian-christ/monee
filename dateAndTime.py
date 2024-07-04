from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

otoday = datetime.now()
today = datetime.now().strftime("%d-%m-%Y")
today_day = datetime.now().day

def strToUnix(s):
    return time.mktime(datetime.strptime(s, "%d-%m-%Y").timetuple())

def strToUnix2(d, m, y):
    s = str(d) + "-" + str(m) + "-" + str(y)
    return time.mktime(datetime.strptime(s, "%d-%m-%Y").timetuple())

def unixToStr(u):
    return datetime.fromtimestamp(int(u)).strftime("%d-%m-%Y")

def month_calc(month, year, direction):
    date = datetime(year, month, 1)
    result = [0,0]

    if direction == 0:
        previous_month = date.replace(day=1) - timedelta(days=1)
        result[0] = int(previous_month.year)
        result[1] = int(previous_month.month)
    elif direction == 1:
        next_month = (date.replace(day=28) + timedelta(days=4)).replace(day=1)
        result[0] = int(next_month.year)
        result[1] = int(next_month.month)
    else:
        print("adjust_month_error")
        return

    return result

def adjust_date(date_str, months):
    date = datetime.strptime(date_str, "%d-%m-%Y")
    adjusted_date = date + relativedelta(months=months)
    adjusted_date_str = adjusted_date.strftime("%d-%m-%Y")
    
    return adjusted_date_str
