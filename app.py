import requests
from forecastiopy import *
import csv
import datetime
from datetime import date
import os

api_key = "29a1e20687b7c4f3463abe9c1fea7843"

Beach = [41.8393, 87.6064]

old_day = datetime.date.today() - datetime.timedelta(1)
unix_time = old_day.strftime("%s")

now = datetime.date.today()
dateformat = datetime.datetime(year=now.year,
                      month=now.month,
                      day=now.day,
                      hour=0,
                      minute=0,
                      second=0).strftime('%Y-%m-%dT%H:%M:%S')

today = now.strftime('%Y-%m-%d')

fio = ForecastIO.ForecastIO(api_key,
                            units=ForecastIO.ForecastIO.UNITS_SI,
                            lang=ForecastIO.ForecastIO.LANG_ENGLISH,
                            latitude=Beach[0], longitude=Beach[1])



uri = 'https://api.darksky.net/forecast/' + api_key + '/' + repr(Beach[0]) + ',' + repr(Beach[1]) + ',' + dateformat
uri2 = 'https://api.darksky.net/forecast/' + api_key + '/' + repr(Beach[0]) + ',' + repr(Beach[1])

r = requests.get(uri)
data = r.json()

r2 = requests.get(uri2)
data2 = r2.json()

datediff = date(now.year, now.month, now.day) - date(now.year, 1, 1)




if fio.has_hourly() is True:
    hourly2 = data2["hourly"]["data"]
    daily = data2["daily"]["data"]

    day = 0

    print(len(daily))

    for obj in daily:
        day += 1
        file_path = repr(now.year) + '/' + repr(datediff.days + day) + '/forecast-daily.csv'
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        f = open(file_path, 'w', newline='')
        hello = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        hello.writerow(obj.keys())
        obj['time'] = datetime.datetime.fromtimestamp(int(obj['time'])).strftime('%Y-%m-%d %H:%M:%S')
        hello.writerow(obj.values())

    day = 0
    count = 0


    for hourdata in hourly2:
        if count >= 24:
            file_path = repr(now.year) + '/' + repr(datediff.days + day) + '/forecast-hourly.csv'
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            f = open(file_path, 'w', newline='')
            hello = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            hello.writerow(hourdata.keys())
            day += 1
            count = 0

        arr = []
        hourdata['time'] = datetime.datetime.fromtimestamp(int(hourdata['time'])).strftime('%Y-%m-%d %H:%M:%S')
        for item in hourdata.keys():
            arr.append(str(hourdata[item]))

        hello.writerow(arr)
        count += 1
else:
	print('No Hourly data')

file_path = repr(now.year) + '/'+ repr(datediff.days) + '/actual-hourly.csv'
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    os.makedirs(directory)


f = open(file_path, 'w', newline='')
hello = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

hello.writerow(data['hourly']['data'][0].keys())
for obj in data['hourly']['data']:
    obj['time'] = datetime.datetime.fromtimestamp(int(obj['time'])).strftime('%Y-%m-%d %H:%M:%S')
    hello.writerow(obj.values())
