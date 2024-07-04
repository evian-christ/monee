from dateAndTime import *

import json

with open('config.json', 'r') as config_file:
    settings = json.load(config_file)

sday = int(settings['month_start_date'])

prev_month = month_calc(otoday.month, otoday.year, 0)[1]
prev_year = month_calc(otoday.month, otoday.year, 0)[0]
next_month = month_calc(otoday.month, otoday.year, 1)[1]
next_year = month_calc(otoday.month, otoday.year, 0)[0]

print(strToUnix2(sday, prev_month, prev_year))

def cur_budget_month():
    if today_day < sday:
        output=month_calc(otoday.month, otoday.year, 0) + [otoday]
    else:
        output=month_calc(otoday.month, otoday.year, 1)
    return output