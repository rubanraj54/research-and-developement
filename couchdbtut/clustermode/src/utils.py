from events import *
from couchdb import Server
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
                              timestamp=int(datetime.datetime.now().strftime('%s')))
    elif event_id == 1:
        return HandleBarVoltageEvent(voltage=random.uniform(1.0, 100.0),
                                    robot_id=_robot_id,
                                     timestamp=int(datetime.datetime.now().strftime('%s')))
    elif event_id == 2:
        return MotorBarVoltageEvent(motor_id=random.randint(1, 10),
                                    voltage=random.uniform(1.0, 100.0),
                                    robot_id=_robot_id,
                                    current=random.uniform(1.0, 100.0),
                                    timestamp=int(datetime.datetime.now().strftime('%s')))
    elif event_id == 3:
        return PoseEvent(x=random.uniform(1.0, 100.0),
                         y=random.uniform(1.0, 100.0),
                         z=random.uniform(1.0, 100.0),
                         theta=random.uniform(1.0, 100.0),
                         robot_id=_robot_id,
                         timestamp=int(datetime.datetime.now().strftime('%s')))
    elif event_id == 4:
        # storing the blob file path
        return RGBEvent(image_base64=big_image_base64_path,blob=False,robot_id=_robot_id,timestamp=int(datetime.datetime.now().strftime('%s')))
    elif event_id == 5:
        # storing the blob file
        return RGBEvent(image_base64=big_image_base64,blob=True,robot_id=_robot_id,timestamp=int(datetime.datetime.now().strftime('%s')))


def run_read_query(query_id,db):
    if query_id is 0:
        # get rgb events(without blob) for last 10 seconds
        # function (doc) {
        # if(doc.name=="rgb_event" && doc.blob==false){
        # emit(doc.timestamp, doc);
        # }
        # }
        return db.view("_design/robot_filters/_view/rgb_withoutblob",limit=1000,descending=True)

    if query_id is 1:
        # function (doc) {
        # if(doc.name=="rgb_event" && doc.blob==true){
        # emit(doc.timestamp, doc);
        # }
        # }
        # get rgb events(with blob) for last 10 seconds
        return db.view("_design/robot_filters/_view/rgb_withblob",limit=1000,descending=True)

    elif query_id is 2:
        #get first 10 PoseEvents generated today
        # function (doc) {
        # if(doc.name=="pose_event"){
        # emit(doc.timestamp, doc);
        # }
        # }
        return db.view("_design/robot_filters/_view/pose_events",limit=10)

    elif query_id is 3:
        # function (doc) {
        # if(doc.name=="location_event" && doc.latitude > 30 && doc.longitude < 50){
        # emit(doc.timestamp, doc);
        # }
        # }
        #get all Location between certain latitude and longitude ranges
        return db.view("_design/robot_filters/_view/location_events")

    return None
