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

    mode = int(sys.argv[3])


    filepath = "/var/executionlogs/"+usecase_name+"/"

    filename = usecase_name+"_"+ datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    logging.basicConfig(filename=(filepath+filename),
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

    db_init()

    if mode is 1:
        for speed_event in SpeedEvent.objects():
            speed_event.delete()
        print "speed documents deleted successfully "
    else:
        for i in range(100):
            _timestamp = datetime.datetime.now()
            speed_event = SpeedEvent(robot_id=robot_id,
                                    speed_id=i,
                                    desired_speed=123.2,
                                    measured_speed=34.34343,
                                    angular_speed=123.324,
                                    timestamp=datetime.datetime.now())
            speed_event.save()
            logging.info("replica_test_write robot_id " + robot_id +" event_id "+ str(i) +" timestamp "+str(_timestamp))
        print "total speed events", len(SpeedEvent.objects())
