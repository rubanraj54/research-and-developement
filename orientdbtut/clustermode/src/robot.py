import time
import datetime
import threading
import Queue
import sys
import timeit
import logging

from utils import *

import os, os.path


def makerelation(robot_id,relation_ship_queue):
    _client = db_connect()
    while(True):
        event = relation_ship_queue.get()
        create_relation(event,_client,robot_id)
        relation_ship_queue.task_done()

def consume(q,robot_id,relation_ship_queue):
    _client = db_connect()
    # _logger = setup_logger('query_execution_logger', "/var/executionlogs/QE_orientdb_robot_id_1"+time_stamp_log_file+".log")
    while(True):
        event,vertex,cluster_id,event_id = q.get()

        start_time = timeit.default_timer()
        stored_event = create_event(cluster_id,'@'+vertex,event,_client)
        end_time = timeit.default_timer()

        logging.info("Robot_id: " + robot_id +" Event : "+str(event_id) +" " + str(end_time - start_time) + " sec ")

        relation_ship_queue.put(stored_event)
        q.task_done()
    running_status = False

def producer(q,event_id,vertex,cluster_id):
    # the main thread will put new events to the queue

    t_end = time.time() + (60 * minutes)
    _frequency = 1.0 if (vertex is "RGBEvent" and event_id is 5) else frequency
    # produce the events for 'n' minutes
    while time.time() < t_end:
        event = get_event(event_id)
        q.put((event,vertex,cluster_id,event_id))
        time.sleep(1.0/_frequency)

    q.join()
    print "produced all events"

def dbsizelogger(robot_id):
    _client = db_connect()
    # _logger = setup_logger('db_size_logger', "/var/executionlogs/DB_size_robot_id_1"+time_stamp_log_file+".log")
    while running_status is True:
        size = _client.db_size()
        logging.info("Robot_id: " + str(robot_id) +" DB size : "+ str(size))
        time.sleep(1)


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

    ### init db
    client = db_connect()

    ### init vertex,edges and root
    init_verteces(client)
    init_edges(client)
    root = init_root_vertex(robot_id,client)

    running_status = True

    time_stamp_log_file = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    verteces = ['LocationEvent','HandleBarVoltageEvent',
    'MototBarVoltageEvent','PoseEvent','RGBEvent','RGBEvent']

    cluster_ids = get_cluster_ids(verteces,client)

    q = Queue.Queue(maxsize = 0)
    relation_ship_queue = Queue.Queue(maxsize = 0)

    # Create number of event producer threads equal to number of events
    for i in range(0,6):
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

    # Thread to log database growth
    db_size_log_thread = threading.Thread(name = "db_size_logger_thread-", target=dbsizelogger, args=(robot_id,))
    db_size_log_thread.daemon = True
    db_size_log_thread.start()

    q.join()
    relation_ship_queue.join()
