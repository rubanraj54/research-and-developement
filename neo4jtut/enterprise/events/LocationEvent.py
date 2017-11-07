
# coding: utf-8

import time
import datetime
import random
import threading
import Queue
import sys
import logging
import timeit

from threading import Lock

from events import LocationEvent
from utils import *

frequency = 30.0 #Herz
mutex = threading.Lock()
minutes = 1

logging.basicConfig(filename="/var/tmp/myapp.log",
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

    t_end = time.time() + 60 * minutes
    # produce the events for 'n' minutes
    while time.time() < t_end:
        # count +=1
        event = get_event(event_id)
        timestamp = datetime.datetime.utcnow()
        q.put((event,timestamp))
        time.sleep(1/frequency)

    # event1 = get_event(1)
    # event2 = get_event(2)
    # event3 = get_event(3)
    # event4 = get_event(4)
    # timestamp = datetime.datetime.utcnow()
    # q.put((event1,timestamp))
    # q.put((event2,timestamp))
    # q.put((event3,timestamp))
    # q.put((event4,timestamp))
    q.join()

if __name__ == '__main__':
    robot_id = sys.argv[1]
    q = Queue.Queue(maxsize = 0)

    threads_num = 10  # number of threads to get event from queue and send to database
    for i in range(threads_num):
        t = threading.Thread(name = "ConsumerThread-"+str(i), target=consume, args=(q,robot_id,))
        t.daemon = True
        t.start()

    # Create number of event producer threads equal to number of events
    for i in range(1,5):
        event_id = i
        t = threading.Thread(name = "ProducerThread-"+str(i), target=producer, args=(q,event_id,))
        t.start()

    #1 thread to produce events
    # producer_one = threading.Thread(name = "ProducerThread1", target=producer, args=(q,))
    # producer_one.start()
    # producer_two = threading.Thread(name = "ProducerThread2", target=producer, args=(q,))
    # producer_two.start()

    q.join()
