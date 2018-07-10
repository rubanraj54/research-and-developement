import random
import datetime
import logging
import time
import pymysql.cursors


fileHandle = open ( 'big_image_base64.txt', 'r' )
big_image_base64 = fileHandle.read()
fileHandle.close()

big_image_base64_path = "/var/data/big_image_base64.txt"
# big_image_base64_path = "/var/data/big_image_base64_2MB.txt"

def db_init():
    connection = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 password='password',
                                 db='mydata',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    return connection

def create_event(connection,event_id,event):
    if event_id == 0:
        with connection.cursor() as cursor:
            # create table `location_events` (robot_id int,latitude float,longitude float,offset float,timestamp int,accuracy float);
            sql = "INSERT INTO `location_events` (`robot_id`,`latitude`,`longitude`,`offset`,`timestamp`,`accuracy`) VALUES (%s, %s,%s, %s,%s, %s)"
            cursor.execute(sql, (event['robot_id'],
            event['latitude'],
            event['longitude'],
            event['offset'],
            event['event_timestamp'],
            event['accuracy']))

            return connection.commit()
    elif event_id == 1:
        with connection.cursor() as cursor:
            # create table `handle_bar_voltage_events` (robot_id int,voltage float,timestamp int);
            sql = "INSERT INTO `handle_bar_voltage_events` (`robot_id`,`voltage`,`timestamp`) VALUES (%s, %s,%s)"
            cursor.execute(sql, (event['robot_id'],
                                event['voltage'],
                                event['event_timestamp']))
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        return connection.commit()

    elif event_id == 2:
        with connection.cursor() as cursor:
            # create table `motor_voltage_events` (robot_id int,voltage float,current float,timestamp int);
            sql = "INSERT INTO `motor_voltage_events` (`robot_id`,`voltage`,`current`,`timestamp`) VALUES (%s,%s, %s,%s)"
            cursor.execute(sql, (event['robot_id'],
                                event['voltage'],
                                event['current'],
                                event['event_timestamp']))
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        return connection.commit()

    elif event_id == 3:
        with connection.cursor() as cursor:
            # create table `pose_events` (robot_id int,x float,y float,z float,theta float,timestamp int);
            sql = "INSERT INTO `pose_events` (`robot_id`,`x`,`y`,`z`,`theta`,`timestamp`) VALUES (%s,%s, %s,%s, %s,%s)"
            cursor.execute(sql, (event['robot_id'],
                                event['x'],
                                event['y'],
                                event['z'],
                                event['theta'],
                                event['event_timestamp']))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        return connection.commit()

    elif event_id == 4:
        # storing the blob file path
        with connection.cursor() as cursor:
            # create table `rgb_events` (robot_id int,image_base64 longtext,blobflag tinyint,timestamp int);
            sql = "INSERT INTO `rgb_events` (`robot_id`,`image_base64`,`blobflag`,`timestamp`) VALUES (%s,%s, %s,%s)"
            cursor.execute(sql, (event['robot_id'],
                                event['image_base64'],
                                event['blobflag'],
                                event['event_timestamp']))
        return connection.commit()

    elif event_id == 5:
        # storing the blob file
        with connection.cursor() as cursor:
            sql = "INSERT INTO `rgb_events` (`robot_id`,`image_base64`,`blobflag`,`timestamp`) VALUES (%s,%s, %s,%s)"
            cursor.execute(sql, (event['robot_id'],
                                event['image_base64'],
                                event['blobflag'],
                                event['event_timestamp']))
            return connection.commit()

def get_event(event_id,_robot_id):
    if event_id == 0:
        return {'latitude' : random.uniform(1.0, 100.0),'longitude' : random.uniform(1.0, 100.0),
                'offset' : random.uniform(1.0, 100.0),'accuracy' : random.uniform(1.0, 100.0) ,
                'event_timestamp' : int(datetime.datetime.now().strftime('%s')),'robot_id' : _robot_id,'name' : "location_event"}
    elif event_id == 1:
        return {'voltage' : random.uniform(1.0, 100.0), 'event_timestamp' : int(datetime.datetime.now().strftime('%s')),
                'robot_id' : _robot_id,'name' : "handle_bar_voltage_event"}
    elif event_id == 2:
        return {'motor_id' : random.randint(1, 10),'voltage' : random.uniform(1.0, 100.0),
                'current' : random.uniform(1.0, 100.0), 'event_timestamp' : int(datetime.datetime.now().strftime('%s')),
                'robot_id' : _robot_id,'name' : "motor_voltage_event"}
    elif event_id == 3:
        return {'x' : random.uniform(1.0, 100.0),'y' : random.uniform(1.0, 100.0),
                'z' : random.uniform(1.0, 100.0),'theta' : random.uniform(1.0, 100.0), 'event_timestamp' : int(datetime.datetime.now().strftime('%s')),
                'robot_id' : _robot_id,'name' : "pose_event"}
    elif event_id == 4:
        # storing the blob file path
        return {'image_base64': big_image_base64_path, 'blobflag' : 0, 'event_timestamp' : int(datetime.datetime.now().strftime('%s')),
                'robot_id' : _robot_id,'name' : "rgb_event"}

    elif event_id == 5:
        # storing the blob file
        return {'image_base64': big_image_base64 , 'blobflag' : 1, 'event_timestamp' : int(datetime.datetime.now().strftime('%s')),
                'robot_id' : _robot_id,'name' : "rgb_event"}

def run_read_query(connection,query_id):
    if query_id is 0:
        # get rgb events(without blob) for last 10 seconds
        end_time_range = datetime.datetime.now()
        start_time_range = int((end_time_range - datetime.timedelta(seconds=10)).strftime('%s'))
        end_time_range = int(end_time_range.strftime('%s'))
        query = "select * from rgb_events where blobflag=0 and timestamp>"+str(start_time_range)+" and timestamp<"+str(end_time_range)+";"

        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    if query_id is 1:
        # get rgb events(with blob) for last 10 seconds
        end_time_range = datetime.datetime.now()
        start_time_range = int((end_time_range - datetime.timedelta(seconds=10)).strftime('%s'))
        end_time_range = int(end_time_range.strftime('%s'))
        query = "select * from rgb_events where blobflag=1 and timestamp>"+str(start_time_range)+" and timestamp<"+str(end_time_range)+";"

        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    elif query_id is 2:
        #get first 10 PoseEvents generated today
        start_time_range = datetime.datetime.combine(datetime.date.today(), datetime.time())
        start_time_range = int(start_time_range.strftime('%s'))

        query = "select * from pose_events where timestamp >  "+str(start_time_range)+ " LIMIT 10;"

        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    elif query_id is 3:
        #get all Location between certain latitude and longitude ranges
        query = "select * from location_events where latitude > "+str(30)+" and longitude < "+str(50)+";"

        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    return None
