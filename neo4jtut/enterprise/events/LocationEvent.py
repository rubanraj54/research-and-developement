
# coding: utf-8

import time
import datetime
import random
import threading
import Queue

from events import LocationEvent
from utils import *

frequency = 60 #Herz

def consume(q):
    while(True):
        # name = threading.currentThread().getName()
        event,timestamp = q.get();
        add_event(event,timestamp.strftime('%Y,%m,%d,%H,%M,%S,%f')[:-3].split(','))
        q.task_done()

def producer(q):
    # the main thread will put new events to the queue

    while True:
        event = LocationEvent(latitude = random.uniform(1.0, 100.0),longitude = random.uniform(1.0, 100.0),
                      offset = random.uniform(1.0, 100.0),accuracy = random.uniform(1.0, 100.0)).save()
        timestamp = datetime.datetime.utcnow()
        q.put((event,timestamp))
        time.sleep(1/frequency)
    q.join()

if __name__ == '__main__':
    q = Queue.Queue(maxsize = 0)

    threads_num = 10  # number of threads to get event from queue and send to database
    for i in range(threads_num):
        t = threading.Thread(name = "ConsumerThread-"+str(i), target=consume, args=(q,))
        t.start()

    #1 thread to generate events
    t = threading.Thread(name = "ProducerThread", target=producer, args=(q,))
    t.start()

    q.join()
