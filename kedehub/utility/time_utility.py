import datetime


def time_to_utc_offset(time):
    utc_time = time.astimezone(datetime.timezone.utc)
    offset = int(time.utcoffset().total_seconds())
    return utc_time, offset


def _time_offset_to_local_time(time, offset):
    timezone = datetime.timezone(datetime.timedelta(seconds=offset))
    return time.replace(tzinfo=datetime.timezone.utc).astimezone(timezone)