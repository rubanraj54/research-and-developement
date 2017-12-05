import uuid
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.columns import UUID,Text,Float,DateTime,Integer,Boolean

class LocationEvent(Model):
    id = UUID(primary_key=True, default=uuid.uuid4)
    name = Text()
    robot_id = Integer()
    latitude = Float()
    longitude = Float()
    offset = Float()
    accuracy = Float()
    event_timestamp = DateTime()

class HandleBarVoltageEvent(Model):
    id = UUID(primary_key=True, default=uuid.uuid4)
    robot_id = Integer()
    name = Text()
    voltage = Float()
    event_timestamp = DateTime()

class MotorBarVoltageEvent(Model):
    id = UUID(primary_key=True, default=uuid.uuid4)
    robot_id = Integer()
    name = Text()
    motor_id = Integer()
    voltage = Float()
    current = Float()
    event_timestamp = DateTime()

class PoseEvent(Model):
    id = UUID(primary_key=True, default=uuid.uuid4)
    robot_id = Integer()
    name = Text()
    x = Float()
    y = Float()
    z = Float()
    theta = Float()
    event_timestamp = DateTime()

class SpeedEvent(Model):
    id = UUID(primary_key=True, default=uuid.uuid4)
    robot_id = Integer()
    name = Text()
    speed_id = Integer(primary_key=True)
    desired_speed = Float()
    measured_speed = Float()
    angular_speed = Float()
    event_timestamp = DateTime()

class DistanceLogEvent(Model):
    id = UUID(primary_key=True, default=uuid.uuid4)
    robot_id = Integer()
    name = Text()
    event_timestamp = DateTime()
    travelled_log = Text()

class RGBEvent(Model):
    id = UUID(primary_key=True, default=uuid.uuid4)
    robot_id = Integer()
    name = Text()
    event_timestamp = DateTime()
    image_base64 = Text()
    blob = Boolean()
