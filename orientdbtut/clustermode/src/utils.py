import pyorient
import random
import datetime
import logging

fileHandle = open ( 'big_image_base64_2MB.txt', 'r' )
big_image_base64 = fileHandle.read()
fileHandle.close()

big_image_base64_path = "/var/data/big_image_base64.txt"

def db_connect():
    client = pyorient.OrientDB("localhost", 2424)
    client.connect("root", "admin")
    client.db_open("Robots", "root", "admin")
    return client

def init_verteces(_client):
    verteces = ['Root','LocationEvent','HandleBarVoltageEvent',
                'MototBarVoltageEvent','PoseEvent','SpeedEvent',
                'DistanceLogEvent','RGBEvent']
    for vertex in verteces:
        try:
            _client.command("create class "+vertex+" extends V")
        except:
            pass

def init_edges(_client):
    edges = ['Event_at']
    for edge in edges:
        try:
            _client.command("create class "+edge+" extends E")
        except:
            pass

def init_root_vertex(robot_id,_client):
    root = _client.command("select * from Root where robot_id=" + robot_id)
    if len(root) < 1:
        root = _client.command("insert into Root set robot_id=" + robot_id)
    return root[0]

def get_cluster_ids(verteces,_client):
    cluster_ids = []
    for vertex in verteces:
        result = _client.command("select * from " + vertex)
        for res in result:
            cluster_id = (res._rid.split(':')[0]).split('#')[1]
            cluster_ids.append(cluster_id)
            break
        if len(result) < 1:
            print "creating dummy vertex to get the cluster_id"
            dummy_vertex = _client.command("insert into " + vertex + " set data='dummy'")[0]
            cluster_id = (dummy_vertex._rid.split(':')[0]).split('#')[1]
            cluster_ids.append(cluster_id)
            _client.record_delete( cluster_id, dummy_vertex._rid )
            print "deleted the dummy vertex"
    return cluster_ids

def create_event(cluster_id,vertex,data,_client):
    event = _client.record_create( cluster_id, { vertex :  data  } )
    return event

def create_relation(event,_client,robot_id):
    _client.command(
    "create edge Event_at from ("
    "select * from Root where robot_id = " + robot_id +
    ") to ("
    "select * from " + event._rid +
    ")"
    )

def get_event(event_id,blob_flag):
    if event_id == 0:
        return {'latitude' : random.uniform(1.0, 100.0),'longitude' : random.uniform(1.0, 100.0),
                      'offset' : random.uniform(1.0, 100.0),'accuracy' : random.uniform(1.0, 100.0) , 'timestamp' : datetime.datetime.now()}
    elif event_id == 1:
        return {'voltage' : random.uniform(1.0, 100.0), 'timestamp' : datetime.datetime.now()}
    elif event_id == 2:
        return {'motor_id' : random.randint(1, 10),'voltage' : random.uniform(1.0, 100.0),
                      'current' : random.uniform(1.0, 100.0), 'timestamp' : datetime.datetime.now()}
    elif event_id == 3:
        return {'x' : random.uniform(1.0, 100.0),'y' : random.uniform(1.0, 100.0),
                      'z' : random.uniform(1.0, 100.0),'theta' : random.uniform(1.0, 100.0), 'timestamp' : datetime.datetime.now()}
    elif event_id == 4:
        return {'image_base64': (big_image_base64 if blob_flag else big_image_base64_path), 'timestamp' : datetime.datetime.now()}

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def get_query(query_id):
    if query_id is 0:
        # get rgb events for last 10 seconds
        current_time = datetime.datetime.now()
        start_time_range = (current_time - datetime.timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')
        end_time_range = current_time.strftime('%Y-%m-%d %H:%M:%S')
        query = "select  image_base64,timestamp,@class from (select expand( out( Event_in )) from Root where robot_id=1) \
                where @class = 'RGBEvent' and timestamp between "\
                +"'"+start_time_range+ "'"+ " and " +"'"+end_time_range+"'"
    elif query_id is 1:
        #get first 10 PoseEvents generated today
        start_time_range = datetime.datetime.combine(datetime.date.today(), datetime.time()).strftime('%Y-%m-%d %H:%M:%S')
        end_time_range = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "select  x,y,z,timestamp,@class from (select expand( out( Event_in )) from Root where robot_id=1) \
                where @class = 'PoseEvent' and timestamp between "\
                +"'"+start_time_range+ "'"+ " and " +"'"+end_time_range+"' LIMIT 10"
    elif query_id is 2:
        #get first 10 PoseEvents generated today
        query = "select  longitude,latitude,timestamp,@class from (select expand( out( Event_in )) from Root where robot_id=1) \
                where @class = 'LocationEvent' and latitude > 30 and longitude < '50'"
                
    return query
