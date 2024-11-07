import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

def display_relative_time(start_time, end_time):
    diff = relativedelta(end_time, start_time)

    if diff.years > 0:
        return f"{diff.years} years ago"
    elif diff.months > 0:
        return f"{diff.months} months ago"
    elif diff.days > 0:
        return f"{diff.days} days ago"
    elif diff.hours > 0:
        return f"{diff.hours} hours ago"
    elif diff.minutes > 0:
        return f"{diff.minutes} minutes ago"
    else:
        seconds = (end_time - start_time).seconds
        return f"{seconds} seconds ago"

def datetime_from_string(datetime_str):
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f%z")

def datetime_to_string(datetime_dt):
    return datetime_dt.strftime("%Y-%m-%d %H:%M:%S %Z")

def get_file_size(file_path):
    file_size = os.path.getsize(file_path)
    if file_size < 1024:
        return '%s bytes'%file_size
    else:
        return '%.2f'%(file_size/1024)
