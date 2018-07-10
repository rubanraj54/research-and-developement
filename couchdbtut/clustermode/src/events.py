from couchdb.mapping import Document, TextField, IntegerField, DateTimeField,FloatField,BooleanField

class LocationEvent(Document):
    name = TextField(default="location_event")
    robot_id = IntegerField()
    latitude = FloatField()
    longitude = FloatField()
    offset = FloatField()
    accuracy = FloatField()
    timestamp = IntegerField()

class HandleBarVoltageEvent(Document):
    robot_id = IntegerField()
    name = TextField(default="handle_bar_voltage_event")
    voltage = FloatField()
    timestamp = IntegerField()

class MotorBarVoltageEvent(Document):
    robot_id = IntegerField()
    name = TextField(default="motor_voltage_event")
    motor_id = IntegerField()
    voltage = FloatField()
    current = FloatField()
    timestamp = IntegerField()

class PoseEvent(Document):
    robot_id = IntegerField()
    name = TextField(default="pose_event")
    x = FloatField()
    y = FloatField()
    z = FloatField()
    theta = FloatField()
    timestamp = IntegerField()

class SpeedEvent(Document):
    robot_id = IntegerField()
    name = TextField(default="speed_event")
    speed_id = IntegerField()
    desired_speed = FloatField()
    measured_speed = FloatField()
    angular_speed = FloatField()
    timestamp = IntegerField()

class DistanceLogEvent(Document):
    robot_id = IntegerField()
    name = TextField(default="distance_log_event")
    timestamp = IntegerField()
    travelled_log = TextField()

class RGBEvent(Document):
    robot_id = IntegerField()
    name = TextField(default="rgb_event")
    timestamp = IntegerField()
    image_base64 = TextField()
    blob = BooleanField()
