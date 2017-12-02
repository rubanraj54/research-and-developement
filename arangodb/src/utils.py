import random
import datetime
import logging
import time
from arango import ArangoClient

fileHandle = open ( 'big_image_base64.txt', 'r' )
big_image_base64 = fileHandle.read()
fileHandle.close()

big_image_base64_path = "/var/data/big_image_base64.txt"
# big_image_base64_path = "/var/data/big_image_base64_2MB.txt"

def db_init():
    client = ArangoClient(
        protocol='http',
        host='localhost',
        port=8529,
        enable_logging=True
    )
    try:
        db = client.create_database('robot')
    except:
        db = client.database('robot')
    collection_init(db)
    print "database is initialized"
    return db

def collection_init(db):
    collections = ['location_event','handle_bar_voltage_event','motor_voltage_event',
    'pose_event','speed_event','distance_log_event','rgb_event']

    for collection in collections:
        try:
            db.create_collection(collection)
        except:
            pass
    print "collections are initialized"

def create_event(db,event_id,event):
    if event_id == 0:
        return db.collection('location_event').insert(event)

    elif event_id == 1:
        return db.collection('handle_bar_voltage_event').insert(event)

    elif event_id == 2:
        return db.collection('motor_voltage_event').insert(event)

    elif event_id == 3:
        return db.collection('pose_event').insert(event)

    elif event_id == 4:
        # storing the blob file path
        return db.collection('rgb_event').insert(event)

    elif event_id == 5:
        # storing the blob file
        return db.collection('rgb_event').insert(event)

def get_event(event_id,_robot_id):
    if event_id == 0:
        return {'latitude' : random.uniform(1.0, 100.0),'longitude' : random.uniform(1.0, 100.0),
                'offset' : random.uniform(1.0, 100.0),'accuracy' : random.uniform(1.0, 100.0) ,
                'event_timestamp' : int(datetime.datetime.now().strftime('%s')),'robot_id' : _robot_id}
    elif event_id == 1:
        return {'voltage' : random.uniform(1.0, 100.0), 'event_timestamp' : int(datetime.datetime.now().strftime('%s')),
                'robot_id' : _robot_id}
    elif event_id == 2:
        return {'motor_id' : random.randint(1, 10),'voltage' : random.uniform(1.0, 100.0),
                'current' : random.uniform(1.0, 100.0), 'event_timestamp' : int(datetime.datetime.now().strftime('%s')),
                'robot_id' : _robot_id}
    elif event_id == 3:
        return {'x' : random.uniform(1.0, 100.0),'y' : random.uniform(1.0, 100.0),
                'z' : random.uniform(1.0, 100.0),'theta' : random.uniform(1.0, 100.0), 'event_timestamp' : int(datetime.datetime.now().strftime('%s')),
                'robot_id' : _robot_id}
    elif event_id == 4:
        # storing the blob file path
        return {'image_base64': big_image_base64_path, 'blob' : False, 'event_timestamp' : int(datetime.datetime.now().strftime('%s')),
                'robot_id' : _robot_id}

    elif event_id == 5:
        # storing the blob file
        return {'image_base64': big_image_base64 , 'blob' : True, 'event_timestamp' : int(datetime.datetime.now().strftime('%s')),
                'robot_id' : _robot_id,'name' : "rgb_event"}

def run_read_query(query_id):
    if query_id is 0:
        # get rgb events(without blob) for last 10 seconds
        end_time_range = datetime.datetime.now()
        start_time_range = (end_time_range - datetime.timedelta(seconds=10))

        return RGBEvent.objects().allow_filtering().filter(event_timestamp__gt=start_time_range).filter(event_timestamp__lt=end_time_range).filter(blob=False)

    if query_id is 1:
        # get rgb events(with blob) for last 10 seconds
        end_time_range = datetime.datetime.now()
        start_time_range = (end_time_range - datetime.timedelta(seconds=10))

        return RGBEvent.objects().allow_filtering().filter(event_timestamp__gt=start_time_range).filter(event_timestamp__lt=end_time_range).filter(blob=True)


    elif query_id is 2:
        #get first 10 PoseEvents generated today
        start_time_range = datetime.datetime.combine(datetime.date.today(), datetime.time())
        end_time_range = datetime.datetime.now()
        return PoseEvent.objects().allow_filtering().filter(event_timestamp__lt=end_time_range).filter(event_timestamp__gt=start_time_range)[:10]

    elif query_id is 3:
        #get all Location between certain latitude and longitude ranges
        return LocationEvent.objects().allow_filtering().filter(latitude__gt=30).filter(longitude__lt=50)

    return None
