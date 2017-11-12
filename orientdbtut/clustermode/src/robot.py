import time
import datetime
import threading
import Queue
import sys
import logging
import timeit

from utils import *

frequency = 120.0 #Herz
minutes = 30

def makerelation(robot_id,relation_ship_queue):
    _client = db_connect()
    while(True):
        event = relation_ship_queue.get()
        create_relation(event,_client,robot_id)
        relation_ship_queue.task_done()

def consume(q,robot_id,relation_ship_queue):
    _client = db_connect()
    while(True):
        event,vertex,cluster_id = q.get()
        stored_event = create_event(cluster_id,'@'+vertex,event,_client)
        relation_ship_queue.put(stored_event)
        q.task_done()

def producer(q,event_id,vertex,cluster_id):
    # the main thread will put new events to the queue

    t_end = time.time() + (2 * 1)
    # produce the events for 'n' minutes
    while time.time() < t_end:
        # start_time = timeit.default_timer()
        event = get_event(event_id)
        # end_time = timeit.default_timer()
        # timestamp = datetime.datetime.now()
        q.put((event,vertex,cluster_id))
        # logging.info("Robot_id: " + robot_id +" Event_id: "+event.name +" " + str(end_time - start_time) + " sec")
        time.sleep(1/frequency)

    q.join()
    print "produced all events"

if __name__ == '__main__':

    robot_id = sys.argv[1]

    ### init db
    client = db_connect()

    ### init vertex,edges and root
    init_verteces(client)
    init_edges(client)
    root = init_root_vertex(robot_id,client)

    verteces = ['LocationEvent','HandleBarVoltageEvent',
    'MototBarVoltageEvent','PoseEvent','RGBEvent']

    cluster_ids = get_cluster_ids(verteces,client)

    q = Queue.Queue(maxsize = 0)
    relation_ship_queue = Queue.Queue(maxsize = 0)

    # Create number of event producer threads equal to number of events
    for i in range(len(verteces)):
        event_id = i
        t = threading.Thread(name = "ProducerThread-"+str(i), target=producer, args=(q,event_id,verteces[i],cluster_ids[i],))
        t.daemon = True
        t.start()

    consumer_thread_count = 10  # number of threads to get event from queue and send to database
    for i in range(consumer_thread_count):
        t = threading.Thread(name = "ConsumerThread-"+str(i), target=consume, args=(q,robot_id,relation_ship_queue,))
        t.daemon = True
        t.start()

    # single thread to make relation between root node and all generated events
    relation_ship_thread = threading.Thread(name = "relation_ship_thread-", target=makerelation, args=(robot_id,relation_ship_queue,))
    relation_ship_thread.daemon = True
    relation_ship_thread.start()

    q.join()
    relation_ship_queue.join()
