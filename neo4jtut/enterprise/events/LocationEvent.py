
# coding: utf-8

import time
import datetime
import random
from events import LocationEvent
from utils import *

frequency = 60 #Herz

for i in range(10):
    event = LocationEvent(latitude = random.uniform(1.0, 100.0),longitude = random.uniform(1.0, 100.0),
                  offset = random.uniform(1.0, 100.0),accuracy = random.uniform(1.0, 100.0)).save()
    add_event(event,datetime.datetime.utcnow().strftime('%Y,%m,%d,%H,%M,%S,%f')[:-3].split(','))
    time.sleep(1/frequency)
