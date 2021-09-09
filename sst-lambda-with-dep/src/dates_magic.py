import datetime
import pytz

def get_current_datetime():
    return datetime.datetime.now(tz=pytz.UTC)