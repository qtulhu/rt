import requests
import numpy as np
import json
import urllib
import queryToDB


s=requests.get('http://user:user@addr.ru/archive/events/detectors/AXXON-SERVER/DeviceIpint.41/SourceEndpoint.video:0:0/future/past?limit=1&type=oneLine')
data = s.json()

length=len(data['events'])
databas=[0]*length

def time_convert(hour):
    a=0
    if (hour<=16):
        new_hour=hour+8
        return (new_hour)
    elif  (hour>16):
        new_hour=(hour+8)-24
        return (a)

def db_form(data1):
    time=data1['events'][0]['timestamp']
    year=time[0:4:1]
    month=time[4:6:1]
    day=time[6:8:1]
    hour=int(time[9:11:1])
    minute=time[11:13:1]
    sec=time[13:15:1]
    indexer=data1['events'][0]['id']
    TYPE=data1['events'][0]['type']
    rectangles=data1['events'][0]['rectangles']
    cam_name='cam_10'
    right_hour=str(time_convert(hour))
    time=(right_hour+":"+minute+":"+sec)
    date=(day+"."+month+"."+year)
    return(cam_name,TYPE,date,time,rectangles)

print("Begin")
event=data
count=0
while(1==1):
    s=requests.get('http://user:user@addr.ru.ru/archive/events/detectors/AXXON-SERVER/DeviceIpint.41/SourceEndpoint.video:0:0/future/past?limit=1&type=oneLine')
    data1 = s.json()
    if(event!=data1):
        count=count+1


        cam_name=str(db_form(data1)[0])
        SENSOR_TYPE=str(db_form(data1)[1])
        DATE_EVENT=str(db_form(data1)[2])
        TIME_EVENT= str(db_form(data1)[3])
        RECTANGLES='0'
        DIRECTION='0'
        HULA_HOOP='0'

        #queryToDB.pushEvent(str(db_form(data1)[0]), str(db_form(data1)[1]), str(db_form(data1)[2]), str(db_form(data1)[3]), str(db_form(data1)[4]),str(DIRECTION), str(HULA_HOOP))
        queryToDB.pushEvent(cam_name, SENSOR_TYPE, DATE_EVENT, TIME_EVENT, RECTANGLES, DIRECTION, HULA_HOOP)
    event=data1
