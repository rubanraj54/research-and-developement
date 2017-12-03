import time
import datetime
import threading
import Queue
import sys
import timeit
import logging

from utils import *

import os, os.path

def read(robot_id,query_id):
    db = db_init()
    t_end = time.time() + (60 * minutes)

    while time.time() < t_end:
        start_time = timeit.default_timer()
        run_read_query(query_id,db)
        end_time = timeit.default_timer()
        logging.info("Robot_id: " + robot_id +" Query_id : "+str(query_id) +" " + str(end_time - start_time) + " sec ")

        time.sleep(1.0/frequency)


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

    read_threads = []
    # single thread to make relation between root node and all generated events
    for i in range(4):
        read_thread = threading.Thread(name = "read_thread-"+str(i), target=read, args=(robot_id,i))
        read_thread.daemon = True
        read_thread.start()
        read_threads.append(read_thread)

    for thread in read_threads:
        thread.join()
