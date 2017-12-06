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

    client = db_init()

    for i in range(100):
        _timestamp = datetime.datetime.now()
        speed_event = [
                    {
                    "measurement": "speed_events",
                    "tags": {
                        "robot_id": robot_id,
                    },
                    "fields": {
                        "speed_id": i,
                        "desired_speed": random.uniform(1.0, 100.0),
                        "measured_speed": random.uniform(1.0, 100.0),
                        "angular_speed": random.uniform(1.0, 100.0),
                        "timestamp": int(datetime.datetime.now().strftime('%s')),
                    }
                    }
                ]
        client.write_points(speed_event)
        logging.info("replica_test_write robot_id " + robot_id +" event_id "+ str(i) +" timestamp "+str(_timestamp))

    print "total speed events", len(list(client.query("select * from speed_events;").get_points(measurement="speed_events")))
