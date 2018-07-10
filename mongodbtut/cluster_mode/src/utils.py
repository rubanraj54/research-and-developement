from events import *
import random
import datetime
import logging
import time

fileHandle = open ( 'big_image_base64.txt', 'r' )
big_image_base64 = fileHandle.read()
fileHandle.close()

big_image_base64_path = "/var/data/big_image_base64.txt"
# big_image_base64_path = "/var/data/big_image_base64_2MB.txt"

def db_init():
    return connect('robot', host='localhost', port=27017)

def create_event(event):
    return event.save()

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


def run_read_query(query_id):
    if query_id is 0:
        # get rgb events(without blob) for last 10 seconds
        end_time_range = datetime.datetime.now()
        start_time_range = (end_time_range - datetime.timedelta(seconds=10))

        return RGBEvent.objects().filter(timestamp__gt=start_time_range).filter(timestamp__lt=end_time_range).filter(blob=False)

    if query_id is 1:
        # get rgb events(with blob) for last 10 seconds
        end_time_range = datetime.datetime.now()
        start_time_range = (end_time_range - datetime.timedelta(seconds=10))

        return RGBEvent.objects().filter(timestamp__gt=start_time_range).filter(timestamp__lt=end_time_range).filter(blob=True)

    elif query_id is 2:
        #get first 10 PoseEvents generated today
        start_time_range = datetime.datetime.combine(datetime.date.today(), datetime.time())
        end_time_range = datetime.datetime.now()
        return PoseEvent.objects().filter(timestamp__lt=end_time_range).filter(timestamp__gt=start_time_range)[:10]

    elif query_id is 3:
        #get all Location between certain latitude and longitude ranges
        return LocationEvent.objects().filter(latitude__gt=30).filter(longitude__lt=50)

    return None
