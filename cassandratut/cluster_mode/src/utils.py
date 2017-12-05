import random
import datetime
import logging
import time
from cassandra.cqlengine.management import sync_table,create_keyspace_simple
from cassandra.cqlengine import connection
from events import *

fileHandle = open ( 'big_image_base64.txt', 'r' )
big_image_base64 = fileHandle.read()
fileHandle.close()

big_image_base64_path = "/var/data/big_image_base64.txt"
# big_image_base64_path = "/var/data/big_image_base64_2MB.txt"

def db_init():
    return connection.setup(['localhost'], "mydb", protocol_version=3,port=9042)

def create_event(event_id,event):
    if event_id == 0:
        return LocationEvent.create(latitude=event['latitude'],
                              robot_id=event['robot_id'],
                              longitude=event['longitude'],
                              offset=event['offset'],
                              accuracy=event['accuracy'],
                              name=event['name'],
                              event_timestamp=event['event_timestamp'])
    elif event_id == 1:
        return HandleBarVoltageEvent.create(voltage=event['voltage'],
                                    robot_id=event['robot_id'],
                                    name=event['name'],
                                    event_timestamp=event['event_timestamp'])
    elif event_id == 2:
        return MotorBarVoltageEvent.create(motor_id=event['motor_id'],
                                    voltage=event['voltage'],
                                    robot_id=event['robot_id'],
                                    current=event['current'],
                                    name=event['name'],
                                    event_timestamp=event['event_timestamp'])
    elif event_id == 3:
        return PoseEvent.create(x=event['x'],
                         y=event['y'],
                         z=event['z'],
                         theta=event['theta'],
                         robot_id=event['robot_id'],
                         name=event['name'],
                         event_timestamp=event['event_timestamp'])
    elif event_id == 4:
        # storing the blob file path
        return RGBEvent.create(image_base64=event['image_base64'],blob=event['blob'],
                        robot_id=event['robot_id'],
                        name=event['name'],
                        event_timestamp=event['event_timestamp'])
    elif event_id == 5:
        # storing the blob file
        return RGBEvent.create(image_base64=event['image_base64'],blob=event['blob'],
                        robot_id=event['robot_id'],
                        name=event['name'],
                        event_timestamp=event['event_timestamp'])

def sync_tables():
    sync_table(LocationEvent)
    sync_table(HandleBarVoltageEvent)
    sync_table(MotorBarVoltageEvent)
    sync_table(PoseEvent)
    sync_table(SpeedEvent)
    sync_table(DistanceLogEvent)
    sync_table(RGBEvent)
    print "created all tables"

def get_event(event_id,_robot_id):
    if event_id == 0:
        return {'latitude' : random.uniform(1.0, 100.0),'longitude' : random.uniform(1.0, 100.0),
                'offset' : random.uniform(1.0, 100.0),'accuracy' : random.uniform(1.0, 100.0) ,
                'event_timestamp' : datetime.datetime.now(),'robot_id' : _robot_id,'name' : "location_event"}
    elif event_id == 1:
        return {'voltage' : random.uniform(1.0, 100.0), 'event_timestamp' : datetime.datetime.now(),
                'robot_id' : _robot_id,'name' : "handle_bar_voltage_event"}
    elif event_id == 2:
        return {'motor_id' : random.randint(1, 10),'voltage' : random.uniform(1.0, 100.0),
                'current' : random.uniform(1.0, 100.0), 'event_timestamp' : datetime.datetime.now(),
                'robot_id' : _robot_id,'name' : "motor_voltage_event"}
    elif event_id == 3:
        return {'x' : random.uniform(1.0, 100.0),'y' : random.uniform(1.0, 100.0),
                'z' : random.uniform(1.0, 100.0),'theta' : random.uniform(1.0, 100.0), 'event_timestamp' : datetime.datetime.now(),
                'robot_id' : _robot_id,'name' : "pose_event"}
    elif event_id == 4:
        # storing the blob file path
        return {'image_base64': big_image_base64_path, 'blob' : False, 'event_timestamp' : datetime.datetime.now(),
                'robot_id' : _robot_id,'name' : "rgb_event"}

    elif event_id == 5:
        # storing the blob file
        return {'image_base64': big_image_base64 , 'blob' : True, 'event_timestamp' : datetime.datetime.now(),
                'robot_id' : _robot_id,'name' : "rgb_event"}



def run_read_query(query_id):
    robot_id = random.randint(1,3)
    if query_id is 0:
        # get rgb events(without blob) for last 10 seconds
        end_time_range = datetime.datetime.now()
        start_time_range = (end_time_range - datetime.timedelta(seconds=10))

        return RGBEvent.objects().allow_filtering().filter(robot_id = robot_id).filter(event_timestamp__gt=start_time_range).filter(event_timestamp__lt=end_time_range).filter(blob=False)

    if query_id is 1:
        # get rgb events(with blob) for last 10 seconds
        end_time_range = datetime.datetime.now()
        start_time_range = (end_time_range - datetime.timedelta(seconds=10))

        return RGBEvent.objects().allow_filtering().filter(robot_id = robot_id).filter(event_timestamp__gt=start_time_range).filter(event_timestamp__lt=end_time_range).filter(blob=True)


    elif query_id is 2:
        #get first 10 PoseEvents generated today
        start_time_range = datetime.datetime.combine(datetime.date.today(), datetime.time())
        end_time_range = datetime.datetime.now()
        return PoseEvent.objects().allow_filtering().filter(robot_id = robot_id).filter(event_timestamp__lt=end_time_range).filter(event_timestamp__gt=start_time_range).limit(10)

    elif query_id is 3:
        #get all Location between certain latitude and longitude ranges
        return LocationEvent.objects().allow_filtering().filter(robot_id = robot_id).filter(latitude__gt=30).filter(longitude__lt=50)

    return None
