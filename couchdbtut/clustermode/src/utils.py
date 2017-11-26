from events import *
from couchdb import Server
import random
import datetime
import logging

fileHandle = open ( 'big_image_base64.txt', 'r' )
big_image_base64 = fileHandle.read()
fileHandle.close()

big_image_base64_path = "/var/data/big_image_base64.txt"

def db_init():
    server = Server('http://admin:admin@localhost:5984')
    try:
        db = server.create('test')
    except:
        db = server['test']
    return db

def create_event(db,event):
    return event.store(db)

def get_event(event_id,_robot_id):
    if event_id == 0:
        return LocationEvent(latitude=random.uniform(1.0, 100.0),
                              robot_id=_robot_id,
                              longitude=random.uniform(1.0, 100.0),
                              offset=random.uniform(1.0, 100.0),
                              accuracy=random.uniform(1.0, 100.0),
                              timestamp=datetime.datetime.now())
    elif event_id == 1:
        return HandleBarVoltageEvent(voltage=random.uniform(1.0, 100.0),
                                    robot_id=_robot_id,
                                     timestamp=datetime.datetime.now())
    elif event_id == 2:
        return MotorBarVoltageEvent(motor_id=random.randint(1, 10),
                                    voltage=random.uniform(1.0, 100.0),
                                    robot_id=_robot_id,
                                    current=random.uniform(1.0, 100.0),
                                    timestamp=datetime.datetime.now())
    elif event_id == 3:
        return PoseEvent(x=random.uniform(1.0, 100.0),
                         y=random.uniform(1.0, 100.0),
                         z=random.uniform(1.0, 100.0),
                         theta=random.uniform(1.0, 100.0),
                         robot_id=_robot_id,
                         timestamp=datetime.datetime.now())
    elif event_id == 4:
        # storing the blob file path
        return RGBEvent(image_base64=big_image_base64_path,blob=False,robot_id=_robot_id,timestamp=datetime.datetime.now())
    elif event_id == 5:
        # storing the blob file
        return RGBEvent(image_base64=big_image_base64,blob=True,robot_id=_robot_id,timestamp=datetime.datetime.now())


def get_query(query_id):
    if query_id is 0:
        # get rgb events(without blob) for last 10 seconds
        current_time = datetime.datetime.now()
        start_time_range = (current_time - datetime.timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')
        end_time_range = current_time.strftime('%Y-%m-%d %H:%M:%S')
        query = "select  image_base64,blob,timestamp,@class from (select expand( out( Event_in )) from Root where robot_id=1) \
                where @class = 'RGBEvent' and blob = false and timestamp between "\
                +"'"+start_time_range+ "'"+ " and " +"'"+end_time_range+"'"

    if query_id is 1:
        # get rgb events(with blob) for last 10 seconds
        current_time = datetime.datetime.now()
        start_time_range = (current_time - datetime.timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')
        end_time_range = current_time.strftime('%Y-%m-%d %H:%M:%S')
        query = "select  image_base64,blob,timestamp,@class from (select expand( out( Event_in )) from Root where robot_id=1) \
                where @class = 'RGBEvent' and blob = true and timestamp between "\
                +"'"+start_time_range+ "'"+ " and " +"'"+end_time_range+"'"

    elif query_id is 2:
        #get first 10 PoseEvents generated today
        start_time_range = datetime.datetime.combine(datetime.date.today(), datetime.time()).strftime('%Y-%m-%d %H:%M:%S')
        end_time_range = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "select  x,y,z,timestamp,@class from (select expand( out( Event_in )) from Root where robot_id=1) \
                where @class = 'PoseEvent' and timestamp between "\
                +"'"+start_time_range+ "'"+ " and " +"'"+end_time_range+"' LIMIT 10"

    elif query_id is 3:
        #get all Pose generated between certain latitude and longitude ranges
        query = "select  longitude,latitude,timestamp,@class from (select expand( out( Event_in )) from Root where robot_id=1) \
                where @class = 'LocationEvent' and latitude > 30 and longitude < '50'"

    return query
