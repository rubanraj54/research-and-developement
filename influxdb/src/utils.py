import random
import datetime
import logging
import time
from influxdb import InfluxDBClient


fileHandle = open ( 'big_image_base64.txt', 'r' )
big_image_base64 = fileHandle.read()
fileHandle.close()

big_image_base64_path = "/var/data/big_image_base64.txt"
# big_image_base64_path = "/var/data/big_image_base64_2MB.txt"

def db_init():
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'robot')
    client.create_database('robot')
    return client

def create_event(client,event):
    return client.write_points(event)

def get_event(event_id,_robot_id):
    if event_id == 0:
        return [
                    {
                    "measurement": "location_events",
                    "tags": {
                        "robot_id": _robot_id,
                    },
                    "fields": {
                        "latitude": random.uniform(1.0, 100.0),
                        "longitude": random.uniform(1.0, 100.0),
                        "offset": random.uniform(1.0, 100.0),
                        "timestamp": int(datetime.datetime.now().strftime('%s')),
                        "accuracy": random.uniform(1.0, 100.0)
                    }
                    }
                ]
    elif event_id == 1:
        return [
                    {
                    "measurement": "handle_bar_voltage_events",
                    "tags": {
                        "robot_id": _robot_id,
                    },
                    "fields": {
                        "voltage": random.uniform(1.0, 100.0),
                        "timestamp": int(datetime.datetime.now().strftime('%s'))
                    }
                    }
                ]

    elif event_id == 2:
        return [
                    {
                    "measurement": "motor_voltage_events",
                    "tags": {
                        "robot_id": _robot_id,
                    },
                    "fields": {
                        "motor_id": random.uniform(1.0, 100.0),
                        "voltage": random.uniform(1.0, 100.0),
                        "current": random.uniform(1.0, 100.0),
                        "timestamp": int(datetime.datetime.now().strftime('%s'))
                    }
                    }
                ]
    elif event_id == 3:
        return [
                    {
                    "measurement": "pose_events",
                    "tags": {
                        "robot_id": _robot_id,
                    },
                    "fields": {
                        "x": random.uniform(1.0, 100.0),
                        "y": random.uniform(1.0, 100.0),
                        "z": random.uniform(1.0, 100.0),
                        "timestamp": int(datetime.datetime.now().strftime('%s')),
                        "theta": random.uniform(1.0, 100.0)
                    }
                    }
                ]
    elif event_id == 4:
        # storing the blob file path
        return [
                    {
                    "measurement": "rgb_events",
                    "tags": {
                        "robot_id": _robot_id,
                    },
                    "fields": {
                        "image_base64": big_image_base64_path,
                        "blob": False,
                        "timestamp": int(datetime.datetime.now().strftime('%s')),
                    }
                    }
                ]
    elif event_id == 5:
        # storing the blob file
        return [
                    {
                    "measurement": "rgb_events",
                    "tags": {
                        "robot_id": _robot_id,
                    },
                    "fields": {
                        "image_base64": big_image_base64,
                        "blob": True,
                        "timestamp": int(datetime.datetime.now().strftime('%s')),
                    }
                    }
                ]

def run_read_query(client,query_id):
    if query_id is 0:
        # get rgb events(without blob) for last 10 seconds
        end_time_range = datetime.datetime.now()
        start_time_range = int((end_time_range - datetime.timedelta(seconds=3000)).strftime('%s'))
        end_time_range = int(end_time_range.strftime('%s'))
        query = "select * from rgb_events where blob=False and timestamp>"+str(start_time_range)+" and timestamp<"+str(end_time_range)+";"
        return client.query(query)
    if query_id is 1:
        # get rgb events(with blob) for last 10 seconds
        end_time_range = datetime.datetime.now()
        start_time_range = int((end_time_range - datetime.timedelta(seconds=3000)).strftime('%s'))
        end_time_range = int(end_time_range.strftime('%s'))
        query = "select * from rgb_events where blob=True and timestamp>"+str(start_time_range)+" and timestamp<"+str(end_time_range)+";"
        return client.query(query)

    elif query_id is 2:
        #get first 10 PoseEvents generated today
        start_time_range = datetime.datetime.combine(datetime.date.today(), datetime.time())
        start_time_range = int(start_time_range.strftime('%s'))

        return client.query("select * from pose_events where timestamp >  "+str(start_time_range)+ " LIMIT 10;")

    elif query_id is 3:
        #get all Location between certain latitude and longitude ranges
        return client.query("select * from location_events where latitude > "+str(30)+" and longitude < "+str(50))

    return None
