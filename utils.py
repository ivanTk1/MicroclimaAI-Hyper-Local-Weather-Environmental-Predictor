import datetime

def current_time_rounded():
    now = datetime.datetime.now()
    # Round to nearest hour
    if now.minute >= 30:
        rounded = now.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)
    else:
        rounded = now.replace(minute=0, second=0, microsecond=0)
    return rounded.strftime('%Y-%m-%d %H:%M:%S')
