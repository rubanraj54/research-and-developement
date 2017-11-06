from events import *

def check_possibility(datetime):
    root = Root.nodes.get_or_none(name="root")
    if root is None:
        Root(name="root").save()

    year = Root.nodes.get_or_none(name="root").year.get_or_none(name=datetime[0])
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

    return True,millisecond


def add_event(event,datetime):
    result = check_possibility(datetime)
    if result[0]:
        event.millisecond.connect(result[1])
