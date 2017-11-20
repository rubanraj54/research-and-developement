import time
import datetime
import threading
import Queue
import sys
import timeit
import logging

from utils import *

import os, os.path

def read(robot_id,query_id):
    t_end = time.time() + (60 * minutes)

    while time.time() < t_end:
        start_time = timeit.default_timer()
        result = run_query(query_id)
        end_time = timeit.default_timer()


        time.sleep(1.0/frequency)


if __name__ == '__main__':

    robot_id = sys.argv[1]

    frequency = float(sys.argv[2]) #Herz

    minutes = int(sys.argv[3])

    blob_flag = True if(sys.argv[4] == "1") else False

    usecase_name = sys.argv[5]

    mode = sys.argv[6]


    filepath = "/var/executionlogs/"+usecase_name+"/"+str(frequency)+"HZ/"+ \
    ("withblob/" if blob_flag else "withoutblob/")

    filename = usecase_name+"_"+ datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')+"_"+ \
    str(frequency)+"hz_"+("withblob.log" if blob_flag else "withoutblob.log")

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    logging.basicConfig(filename=(filepath+filename),
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

    for speed_event in SpeedEvent.nodes:
        speed_event.delete()

    # if mode is 1 do write process
    if mode is "1":
        for i in range(100):
            SpeedEvent(speed_id = i,desired_speed = random.uniform(1.0, 100.0),
            measured_speed = random.uniform(1.0, 100.0),angular_speed = random.uniform(1.0, 100.0),
            timestamp = datetime.datetime.now()).save()

            logging.info("replica_test_write robot_id " + robot_id +" event_id "+ str(i) +" timestamp "+str(datetime.datetime.now()))
    # if mode is 2, check nodes are replicated in other robot
    else:
        speed_ids = range(100)
        while len(speed_ids) > 0:
            speed_ids_copy = speed_ids
            for _speed_id in speed_ids_copy:
                #if a node is found in other robot (means replicated), then remove its id from array
                if SpeedEvent.nodes.get_or_none(speed_id=_speed_id) is not None:
                    speed_ids.remove(_speed_id)
