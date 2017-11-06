
# coding: utf-8

import time
import datetime
import random
import threading
import Queue
import sys

from threading import Lock

from events import LocationEvent
from utils import *

frequency = 30.0 #Herz
mutex = threading.Lock()
def consume(q,robot_id):
    while(True):
        # name = threading.currentThread().getName()
        event,timestamp = q.get();
        mutex.acquire(1)
        # millisecond  = check_possibility(timestamp.strftime('%Y,%m,%d,%H,%M,%S,%f')[:-3].split(','),robot_id)
        add_event(event,timestamp.strftime('%Y,%m,%d,%H,%M,%S,%f')[:-3].split(','),robot_id)
        mutex.release()
        q.task_done()

def producer(q):
    # the main thread will put new events to the queue

    t_end = time.time() + 30 * 1
    while time.time() < t_end:
        # count +=1
        event = get_event(random.randint(1,4))
        timestamp = datetime.datetime.utcnow()
        q.put((event,timestamp))
        time.sleep(1/frequency)
    q.join()

if __name__ == '__main__':
    robot_id = sys.argv[1]
    q = Queue.Queue(maxsize = 0)

    threads_num = 10  # number of threads to get event from queue and send to database
    for i in range(threads_num):
        t = threading.Thread(name = "ConsumerThread-"+str(i), target=consume, args=(q,robot_id,))
        t.daemon = True
        t.start()

    #1 thread to generate events
    t = threading.Thread(name = "ProducerThread", target=producer, args=(q,))
    t.start()

    q.join()
