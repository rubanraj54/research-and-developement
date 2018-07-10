import time
import datetime
import threading
import Queue
import sys
import timeit
import logging
import os, os.path

from utils import *

if __name__ == '__main__':

    robot_id = sys.argv[1]

    usecase_name = sys.argv[2]

    filepath = "/var/executionlogs/"+usecase_name+"/"

    filename = usecase_name+"_"+ datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    logging.basicConfig(filename=(filepath+filename),
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)


    for i in range(100):
        connection = db_init()
        _timestamp = datetime.datetime.now()
        # create table `speed_events` (robot_id int,speed_id int,desired_speed float,measured_speed float,angular_speed float,event_timestamp int);
        event = {'speed_id': i,'desired_speed' : random.uniform(1.0, 100.0),'measured_speed' : random.uniform(1.0, 100.0),
                'angular_speed' : random.uniform(1.0, 100.0),'event_timestamp' : int(datetime.datetime.now().strftime('%s')),
                'robot_id' : robot_id}

        with connection.cursor() as cursor:
            # create table `location_events` (robot_id int,latitude float,longitude float,offset float,timestamp int,accuracy float);
            sql = "INSERT INTO `speed_events` (`robot_id`,`speed_id`,`desired_speed`,`measured_speed`,`angular_speed`,`event_timestamp`) VALUES (%s, %s,%s, %s,%s, %s)"
            cursor.execute(sql, (event['robot_id'],
            event['speed_id'],
            event['desired_speed'],
            event['measured_speed'],
            event['angular_speed'],
            event['event_timestamp']))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        logging.info("replica_test_write robot_id " + robot_id +" event_id "+ str(i) +" timestamp "+str(_timestamp))
        connection.close()

    connection = db_init()
    with connection.cursor() as cursor:
        print "total speed events", cursor.execute("select * from speed_events;")
    connection.close()
