
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

import os, os.path

def makerelation(robot_id,relation_ship_queue):
    root = init_root_node(robot_id)
    print 'making RelationshipTo'
    while(True):
        event = relation_ship_queue.get()
        create_relation(root,event)
        relation_ship_queue.task_done()
    print 'made all relations'

def consume(q,robot_id):
    while(True):
        # name = threading.currentThread().getName()
        event,event_id = q.get();
        start_time = timeit.default_timer()
        stored_event = add_event(event,robot_id)
        end_time = timeit.default_timer()
        logging.info("Robot_id: " + robot_id +" Event_id: "+str(event_id) +" " + str(end_time - start_time) + " sec")
        relation_ship_queue.put(stored_event)
        q.task_done()

def producer(q,event_id):
    # the main thread will put new events to the queue

    t_end = time.time() + (60 * minutes)
    # produce the events for 'n' minutes
    while time.time() < t_end:
        event = get_event(event_id)
        q.put((event,event_id))
        time.sleep(1.0 if (event_id is 6) else (1/frequency))

    print "produced all events"
    q.join()

if __name__ == '__main__':

    robot_id = sys.argv[1]
    frequency = float(sys.argv[2]) #Herz

    minutes = int(sys.argv[3])

    usecase_name = sys.argv[4]

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

    q = Queue.Queue(maxsize = 0)
    relation_ship_queue = Queue.Queue(maxsize = 0)

    # Create number of event producer threads equal to number of events
    for i in range(1,7):
        event_id = i
        t = threading.Thread(name = "ProducerThread-"+str(i), target=producer, args=(q,event_id,))
        t.start()

    # number of threads to get event from queue and send to database
    threads_num = 15
    for i in range(threads_num):
        t = threading.Thread(name = "ConsumerThread-"+str(i), target=consume, args=(q,robot_id,))
        t.daemon = True
        t.start()

    relation_ship_thread = threading.Thread(name = "relation_ship_thread-", target=makerelation, args=(robot_id,relation_ship_queue,))
    relation_ship_thread.daemon = True
    relation_ship_thread.start()

    q.join()
    relation_ship_queue.join()
