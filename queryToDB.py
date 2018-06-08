# -*- coding: utf-8 -*-
import sqlite3 as lite

#cam_name=cam_10(строго как в базе данных)

def pushEvent(cam_name, SENSOR_TYPE, DATE_EVENT, TIME_EVENT, RECTANGLES, DIRECTION, HULA_HOOP):

    #print('cam_name:',cam_name,type(cam_name))
    #print('SENSOR_TYPE:',SENSOR_TYPE,type(SENSOR_TYPE))
    #print('DATE_EVENT:',DATE_EVENT,type(DATE_EVENT))
    #print('TIME_EVENT:',TIME_EVENT,type(TIME_EVENT))
    #print('RECTANGLES:',RECTANGLES,type(RECTANGLES))
    #print('DIRECTION:',DIRECTION,type(DIRECTION))
    #print('HULA_HOOP:',HULA_HOOP,type(HULA_HOOP))

    try:
        conn = lite.connect('parkingson.db')
        cursor = conn.cursor()
        cursor.executescript("INSERT INTO cam_10 (SENSOR_TYPE, DATE_EVENT, TIME_EVENT, RECTANGLES, DIRECTION, HULA_HOOP) VALUES ('%s','%s','%s','%s','%s','%s')"%(SENSOR_TYPE, DATE_EVENT, TIME_EVENT, RECTANGLES, DIRECTION, HULA_HOOP))
        conn.commit()
        print("Ok")
    except lite.Error:
        if conn:
            conn.rollback()
        print ("Error")

    finally:
        if conn:
            conn.close()


def getEvent(cam_name):
    try:
        conn = lite.connect('parkingson.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cam_name WHERE id = (SELECT max(id) FROM cam_name)')
        conn.commit()
        unitCam = cursor.fetchone()
        return(unitCam)
    except lite.Error:
        if conn:
            conn.rollback()
        print ("Error")

    finally:
        if conn:
            conn.close()
