import time
import datetime
import threading
import Queue
import sys
import timeit
import logging

from utils import *

import os, os.path

def consume(q):
    db = db_init()
    # _logger = setup_logger('query_execution_logger', "/var/executionlogs/QE_orientdb_robot_id_1"+time_stamp_log_file+".log")
    while(True):
        event,event_id = q.get()

        start_time = timeit.default_timer()
        stored_event = create_event(db,event)
        end_time = timeit.default_timer()
        logging.info("Robot_id: " + robot_id +" Event : "+str(event_id) +" " + str(end_time - start_time) + " sec ")
        q.task_done()

    print "all events consumed by database"

def producer(q,event_id):
    # the main thread will put new events to the queue

    t_end = time.time() + (60 * minutes)
    _frequency = 1.0 if (event_id is 5) else frequency
    # produce the events for 'n' minutes
    while time.time() < t_end:
        event = get_event(event_id,robot_id)
        q.put((event,event_id))
        time.sleep(1.0/_frequency)
    q.join()

    print "produced all events"

if __name__ == '__main__':

    robot_id = sys.argv[1]

    frequency = float(sys.argv[2]) #Herz

    minutes = int(sys.argv[3])

    usecase_name = sys.argv[4]

    print datetime.datetime.now()

    filepath = "/var/executionlogs/"+usecase_name+"/"+str(frequency)+"HZ/"

    filename = usecase_name+"_"+ datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')+"_"+ \
            str(frequency)+"_hz.log"

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    logging.basicConfig(filename=(filepath+filename),
                                filemode='a',
                                format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                datefmt='%H:%M:%S',
                                level=logging.INFO)

    running_status = True

    q = Queue.Queue(maxsize = 0)

    # Create number of event producer threads equal to number of events
    for i in range(0,6):
        event_id = i
        t = threading.Thread(name = "ProducerThread-"+str(i), target=producer, args=(q,event_id,))
        t.start()

    consumer_thread_count = 10  # number of threads to get event from queue and send to database
    for i in range(consumer_thread_count):
        t = threading.Thread(name = "ConsumerThread-"+str(i), target=consume, args=(q,))
        t.daemon = True
        t.start()

    q.join()
