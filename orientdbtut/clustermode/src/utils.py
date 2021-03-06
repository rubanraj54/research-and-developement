import pyorient
import random
import datetime
import logging

fileHandle = open ( 'big_image_base64.txt', 'r' )
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

def get_event(event_id):
    if event_id == 0:
        # return "insert into LocationEvent set latitude="+str(random.uniform(1.0, 100.0))+",longitude="+str(random.uniform(1.0, 100.0))+",offset="+str(random.uniform(1.0, 100.0)) \
        #         +",accuracy="+str(random.uniform(1.0, 100.0))+",timestamp=DATE(\""+str(datetime.datetime.now())+"\")"
        return {'latitude' : random.uniform(1.0, 100.0),'longitude' : random.uniform(1.0, 100.0),
                      'offset' : random.uniform(1.0, 100.0),'accuracy' : random.uniform(1.0, 100.0) ,
                      'timestamp' : datetime.datetime.now()}
    elif event_id == 1:
        # return "insert into HandleBarVoltageEvent set voltage="+str(random.uniform(1.0, 100.0))+",timestamp=DATE(\""+str(datetime.datetime.now())+"\")"
        return {'voltage' : random.uniform(1.0, 100.0), 'timestamp' : datetime.datetime.now()}
    elif event_id == 2:
        # return "insert into MototBarVoltageEvent set motor_id="+str(random.randint(1, 10))+",voltage="+str(random.uniform(1.0, 100.0))+",current="+str(random.uniform(1.0, 100.0)) \
        #         +",timestamp=DATE(\""+str(datetime.datetime.now())+"\")"
        return {'motor_id' : random.randint(1, 10),'voltage' : random.uniform(1.0, 100.0),
                      'current' : random.uniform(1.0, 100.0), 'timestamp' : datetime.datetime.now()}
    elif event_id == 3:
        # return "insert into PoseEvent set x="+str(random.uniform(1.0, 100.0))+",y="+str(random.uniform(1.0, 100.0))+",z="+str(random.uniform(1.0, 100.0)) \
        #         +",timestamp=DATE(\""+str(datetime.datetime.now())+"\")"
        return {'x' : random.uniform(1.0, 100.0),'y' : random.uniform(1.0, 100.0),
                      'z' : random.uniform(1.0, 100.0),'theta' : random.uniform(1.0, 100.0), 'timestamp' : datetime.datetime.now()}
    elif event_id == 4:
        # storing the blob file path
        # return "insert into RGBEvent set image_base64=\""+big_image_base64_path+"\",blob=false,timestamp=DATE(\""+str(datetime.datetime.now())+"\")"
        return {'image_base64': big_image_base64_path, 'blob' : False, 'timestamp' : datetime.datetime.now()}

    elif event_id == 5:
        # storing the blob file
        # return "insert into RGBEvent set image_base64=\""+big_image_base64+"\",blob=true,timestamp=DATE(\""+str(datetime.datetime.now())+"\")"
        return {'image_base64': big_image_base64 , 'blob' : True, 'timestamp' : datetime.datetime.now()}

# this function is not used anywhere
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
        # get rgb events(without blob) for last 10 seconds
        current_time = datetime.datetime.now()
        start_time_range = (current_time - datetime.timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')
        end_time_range = current_time.strftime('%Y-%m-%d %H:%M:%S')
        query = "select  image_base64,blob,timestamp,@class from (select expand( out( Event_in )) from Root where robot_id=1) \
                where @class = 'RGBEvent' and blob = false and timestamp between "\
                +"'"+start_time_range+ "'"+ " and " +"'"+end_time_range+"'"

    if query_id is 1:
        # get rgb events(with blob) for last 10 seconds
        current_time = datetime.datetime.now()
        start_time_range = (current_time - datetime.timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')
        end_time_range = current_time.strftime('%Y-%m-%d %H:%M:%S')
        query = "select  image_base64,blob,timestamp,@class from (select expand( out( Event_in )) from Root where robot_id=1) \
                where @class = 'RGBEvent' and blob = true and timestamp between "\
                +"'"+start_time_range+ "'"+ " and " +"'"+end_time_range+"'"

    elif query_id is 2:
        #get first 10 PoseEvents generated today
        start_time_range = datetime.datetime.combine(datetime.date.today(), datetime.time()).strftime('%Y-%m-%d %H:%M:%S')
        end_time_range = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "select  x,y,z,timestamp,@class from (select expand( out( Event_in )) from Root where robot_id=1) \
                where @class = 'PoseEvent' and timestamp between "\
                +"'"+start_time_range+ "'"+ " and " +"'"+end_time_range+"' LIMIT 10"

    elif query_id is 3:
        #get all Pose generated between certain latitude and longitude ranges
        query = "select  longitude,latitude,timestamp,@class from (select expand( out( Event_in )) from Root where robot_id=1) \
                where @class = 'LocationEvent' and latitude > 30 and longitude < '50'"

    return query
