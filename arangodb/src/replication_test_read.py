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

    db = db_init()
    for speed_event in db.collection('speed_events'):
        db.collection('speed_events').delete(speed_event)

    print "speed documents deleted successfully "

    speed_ids = range(100)

    while len(speed_ids) > 0:
        speed_ids_copy = speed_ids
        for _speed_id in speed_ids_copy:
            #if a node is found in other robot (means replicated), then remove its id from array
            if db.collection('speed_events').find({'speed_id':_speed_id}).count() > 0:
            # if SpeedEvent.objects().allow_filtering().filter(speed_id = _speed_id).count() > 0:
                logging.info("replica_test_read robot_id " + robot_id +" event_id "+ str(_speed_id) +" timestamp "+str(datetime.datetime.now()))
                speed_ids.remove(_speed_id)
    print "replication test read finished"
