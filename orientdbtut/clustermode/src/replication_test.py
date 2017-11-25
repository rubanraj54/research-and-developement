import time
import datetime
import threading
import Queue
import sys
import timeit
import logging

from utils import *

import os, os.path


if __name__ == '__main__':

    robot_id = sys.argv[1]

    usecase_name = sys.argv[2]

    mode = sys.argv[3]


    filepath = "/var/executionlogs/"+usecase_name+"/"

    filename = usecase_name+"_"+ datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    logging.basicConfig(filename=(filepath+filename),
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

    client = db_connect()

    init_verteces(client)
    init_edges(client)
    root = init_root_vertex(robot_id,client)

    client.command("delete vertex SpeedEvent")

    # if mode is 1 do write process
    if mode is "1":
        for i in range(100):
            _timestamp = datetime.datetime.now()
            event_query = "insert into SpeedEvent set speed_id="+str(i)+",measured_speed=24.3453,angular_speed=32.234,timestamp=DATE(\""+str(_timestamp)+"\")"
            # print client.command(event_query)[0]._rid
            # break
            logging.info("replica_test_write robot_id " + robot_id +" event_id "+ str(i) +" timestamp "+str(_timestamp))
    # if mode is 2, check nodes are replicated in other robot
    else:
        speed_ids = range(100)
        while len(speed_ids) > 0:
            speed_ids_copy = speed_ids
            for _speed_id in speed_ids_copy:
                #if a node is found in other robot (means replicated), then remove its id from array
                if len(client.command("select * from SpeedEvent where speed_id=" + str(_speed_id))) > 0:
                    logging.info("replica_test_read robot_id " + robot_id +" event_id "+ str(_speed_id) +" timestamp "+str(datetime.datetime.now()))
                    speed_ids.remove(_speed_id)
