
# coding: utf-8

import time
import datetime
import random
import threading
import Queue
import sys
import logging
import timeit
from neomodel import db
from threading import Lock

from events import LocationEvent
from utils import *

frequency = 30.0 #Herz
mutex = threading.Lock()
minutes = 1

logging.basicConfig(filename="/var/tmp/query_execution_"+datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')+".log",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

# logger.setLevel(logging.WARNING)

def consume(q,robot_id):
    while(True):
        # name = threading.currentThread().getName()
        event,timestamp = q.get();
        mutex.acquire(1)
        start_time = timeit.default_timer()
        add_event(event,timestamp.strftime('%Y,%m,%d,%H,%M,%S,%f')[:-3].split(','),robot_id)
        logging.info("Robot id: " + robot_id +" Event id: "+event.name +" took " + str(timeit.default_timer() - start_time) + " sec")
        mutex.release()
        q.task_done()

def producer(q,event_id):
    # the main thread will put new events to the queue

    t_end = time.time() + 2 * minutes
    # produce the events for 'n' minutes
    while time.time() < t_end:
        event = get_event(event_id)
        timestamp = datetime.datetime.utcnow()
        q.put((event,timestamp))
        time.sleep(1/frequency)

    q.join()

if __name__ == '__main__':
    robot_id = sys.argv[1]
    q = Queue.Queue(maxsize = 0)
    results, meta = db.cypher_query("PROFILE match (n:LocationEvent) return n LIMIT 1", None)
    # print LocationEvent.inflate(results[0][0]).longitude
    threads_num = 10  # number of threads to get event from queue and send to database
    for i in range(threads_num):
        t = threading.Thread(name = "ConsumerThread-"+str(i), target=consume, args=(q,robot_id,))
        t.daemon = True
        t.start()

    # Create number of event producer threads equal to number of events
    for i in range(1,6):
        event_id = i
        t = threading.Thread(name = "ProducerThread-"+str(i), target=producer, args=(q,event_id,))
        t.start()

    q.join()
