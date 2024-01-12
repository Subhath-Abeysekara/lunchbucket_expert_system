import datetime
import pytz

def get_utc_time_count():
    current_time = datetime.datetime.now(pytz.utc)
    hours = int(current_time.strftime('%H'))
    minutes = int(current_time.strftime('%M'))
    return hours * 60 + minutes

