from events import *
import random
import datetime

random.seed(9001)

# Read the big image base64 content from text file and store it in a variable for later use
fileHandle = open ( 'big_image_base64.txt', 'r' )
big_image_base64 = fileHandle.read()
fileHandle.close()
big_image_base64_path = "/var/data/big_image_base64.txt"
def check_possibility(datetime,_robot_id):
    root = Root.nodes.get_or_none(name="root",robot_id=_robot_id)
    if root is None:
        root = Root(name="root",robot_id=_robot_id).save()

    year = root.year.get_or_none(name=datetime[0])
    if year is None:
        year = Year(name=datetime[0]).save()
        root.year.connect(year)

    month = year.month.get_or_none(name=datetime[1])
    if month is None:
        month = Month(name=datetime[1]).save()
        year.month.connect(month)

    day = month.day.get_or_none(name=datetime[2])
    if day is None:
        day = Day(name=datetime[2]).save()
        month.day.connect(day)

    hour = day.hour.get_or_none(name=datetime[3])
    if hour is None:
        hour = Hour(name=datetime[3]).save()
        day.hour.connect(hour)

    minute = hour.minute.get_or_none(name=datetime[4])
    if minute is None:
        minute = Minute(name=datetime[4]).save()
        hour.minute.connect(minute)

    second = minute.second.get_or_none(name=datetime[5])
    if second is None:
        second = Second(name=datetime[5]).save()
        minute.second.connect(second)

    millisecond = second.millisecond.get_or_none(name=datetime[6])
    if millisecond is None:
        millisecond = MilliSecond(name=datetime[6]).save()
        second.millisecond.connect(millisecond)

    return millisecond

def init_root_node(_robot_id):
    root = Root.nodes.get_or_none(name="root",robot_id=_robot_id)
    if root is None:
        root = Root(name="root",robot_id=_robot_id).save()
    return root

def create_relation(root,event):
    event.root.connect(root)

def add_event(event,robot_id):
    return event.save()
    # millisecond = check_possibility(timestamp,robot_id)
    # event.millisecond.connect(millisecond)

def get_event(event_id,blob_flag):
    if event_id == 1:
        return LocationEvent(latitude = random.uniform(1.0, 100.0),longitude = random.uniform(1.0, 100.0),
                      offset = random.uniform(1.0, 100.0),accuracy = random.uniform(1.0, 100.0),timestamp = datetime.datetime.now())
    elif event_id == 2:
        return HandleBarVoltageEvent(voltage = random.uniform(1.0, 100.0),timestamp = datetime.datetime.now())
    elif event_id == 3:
        return MototBarVoltageEvent(motor_id = random.randint(1, 10),voltage = random.uniform(1.0, 100.0),
                      current = random.uniform(1.0, 100.0),timestamp = datetime.datetime.now())
    elif event_id == 4:
        return PoseEvent(x = random.uniform(1.0, 100.0),y = random.uniform(1.0, 100.0),
                      z = random.uniform(1.0, 100.0),theta = random.uniform(1.0, 100.0),
                      timestamp = datetime.datetime.now())
    elif event_id == 5:
        return RGBEvent(image_base64=(big_image_base64 if blob_flag else big_image_base64_path),timestamp = datetime.datetime.now())
