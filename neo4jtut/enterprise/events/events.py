from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,BooleanProperty,
    UniqueIdProperty, RelationshipTo, RelationshipFrom,cardinality,FloatProperty,DateTimeProperty,db)

config.DATABASE_URL = 'bolt://neo4j:admin@localhost:7687'
config.NEOMODEL_CYPHER_DEBUG = 0

class Root(StructuredNode):
    robot_id = IntegerProperty()
    name = StringProperty(unique_index=True, required=True)

class Year(StructuredNode):
    name = StringProperty(index=True, default=0)
    next_year = RelationshipTo('Year', 'NEXT')
    month = RelationshipTo('Month', 'CHILD')

class Month(StructuredNode):
    name = StringProperty(index=True, default=0)
    next_month = RelationshipTo('Month', 'NEXT')
    day = RelationshipTo('Day', 'CHILD')

class Day(StructuredNode):
    name = StringProperty(index=True, default=0)
    next_day = RelationshipTo('Day', 'NEXT')
    hour = RelationshipTo('Hour', 'CHILD')

class Hour(StructuredNode):
    name = StringProperty(index=True, default=0)
    next_hour = RelationshipTo('Hour', 'NEXT')
    minute = RelationshipTo('Minute', 'CHILD')

class Minute(StructuredNode):
    name = StringProperty(index=True, default=0)
    next_minute = RelationshipTo('Minute', 'NEXT')
    second = RelationshipTo('Second', 'CHILD')

class Second(StructuredNode):
    name = StringProperty(index=True, default=0)
    next_second = RelationshipTo('Second', 'NEXT')
    millisecond = RelationshipTo('MilliSecond', 'CHILD')

class MilliSecond(StructuredNode):
    name = StringProperty(index=True, default=0)
    next_millisecond = RelationshipTo('MilliSecond', 'NEXT')

class LocationEvent(StructuredNode):
    name = StringProperty(index=True, default="location_event")
    latitude = FloatProperty()
    longitude = FloatProperty()
    offset = FloatProperty()
    accuracy = FloatProperty()
    timestamp = DateTimeProperty()
    root = RelationshipTo('Root', 'EVENT_AT')

class HandleBarVoltageEvent(StructuredNode):
    name = StringProperty(index=True, default="handle_bar_voltage_event")
    voltage = FloatProperty()
    timestamp = DateTimeProperty()
    root = RelationshipTo('Root', 'EVENT_AT')

class MototBarVoltageEvent(StructuredNode):
    name = StringProperty(index=True, default="motor_voltage_event")
    motor_id = IntegerProperty()
    voltage = FloatProperty()
    current = FloatProperty()
    timestamp = DateTimeProperty()
    root = RelationshipTo('Root', 'EVENT_AT')

class PoseEvent(StructuredNode):
    name = StringProperty(index=True, default="pose_event")
    x = FloatProperty()
    y = FloatProperty()
    z = FloatProperty()
    theta = FloatProperty()
    timestamp = DateTimeProperty()
    root = RelationshipTo('Root', 'EVENT_AT')

class SpeedEvent(StructuredNode):
    name = StringProperty(index=True, default="speed_event")
    speed_id = IntegerProperty()
    desired_speed = FloatProperty()
    measured_speed = FloatProperty()
    angular_speed = FloatProperty()
    timestamp = DateTimeProperty()
    root = RelationshipTo('Root', 'EVENT_AT')

class DistanceLogEvent(StructuredNode):
    name = StringProperty(index=True, default="distance_log_event")
    timestamp = DateTimeProperty()
    travelled_log = StringProperty()
    root = RelationshipTo('Root', 'EVENT_AT')

class RGBEvent(StructuredNode):
    name = StringProperty(index=True, default="rgb_event")
    timestamp = DateTimeProperty()
    image_base64 = StringProperty()
    blob = BooleanProperty()
    root = RelationshipTo('Root', 'EVENT_AT')
