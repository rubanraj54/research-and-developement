from mongoengine import *

class LocationEvent(Document):
    name = StringField(default="location_event")
    robot_id = IntField()
    latitude = FloatField()
    longitude = FloatField()
    offset = FloatField()
    accuracy = FloatField()
    timestamp = DateTimeField()

class HandleBarVoltageEvent(Document):
    robot_id = IntField()
    name = StringField(default="handle_bar_voltage_event")
    voltage = FloatField()
    timestamp = DateTimeField()

class MotorBarVoltageEvent(Document):
    robot_id = IntField()
    name = StringField(default="motor_voltage_event")
    motor_id = IntField()
    voltage = FloatField()
    current = FloatField()
    timestamp = DateTimeField()

class PoseEvent(Document):
    robot_id = IntField()
    name = StringField(default="pose_event")
    x = FloatField()
    y = FloatField()
    z = FloatField()
    theta = FloatField()
    timestamp = DateTimeField()

class SpeedEvent(Document):
    robot_id = IntField()
    name = StringField(default="speed_event")
    speed_id = IntField()
    desired_speed = FloatField()
    measured_speed = FloatField()
    angular_speed = FloatField()
    timestamp = DateTimeField()

class DistanceLogEvent(Document):
    robot_id = IntField()
    name = StringField(default="distance_log_event")
    timestamp = DateTimeField()
    travelled_log = StringField()

class RGBEvent(Document):
    robot_id = IntField()
    name = StringField(default="rgb_event")
    timestamp = DateTimeField()
    image_base64 = StringField()
    blob = BooleanField()
