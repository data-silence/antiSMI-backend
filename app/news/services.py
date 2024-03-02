from datetime import datetime, timedelta


def get_time_period(user_date: datetime.date = datetime.now()) -> tuple: #  + timedelta(hours=3)
    time_now = user_date

    start = datetime(year=time_now.year, month=time_now.month, day=time_now.day, hour=00, minute=00)
    end = datetime(year=time_now.year, month=time_now.month, day=time_now.day, hour=23, minute=59)

    if time_now.day == datetime.today():
        if time_now.hour in range(0, 10):
            start = datetime(year=time_now.year, month=time_now.month, day=time_now.day - 1, hour=20, minute=56)
            end = datetime(year=time_now.year, month=time_now.month, day=time_now.day - 1, hour=22, minute=55)
        if time_now.hour in range(10, 14):
            start = datetime(year=time_now.year, month=time_now.month, day=time_now.day - 1, hour=22, minute=56)
            end = datetime(year=time_now.year, month=time_now.month, day=time_now.day, hour=8, minute=55)
        if time_now.hour in range(14, 18):
            start = datetime(year=time_now.year, month=time_now.month, day=time_now.day, hour=8, minute=56)
            end = datetime(year=time_now.year, month=time_now.month, day=time_now.day, hour=12, minute=55)
        if time_now.hour in range(18, 22):
            start = datetime(year=time_now.year, month=time_now.month, day=time_now.day, hour=12, minute=56)
            end = datetime(year=time_now.year, month=time_now.month, day=time_now.day, hour=16, minute=55)
        if time_now.hour in range(22, 24):
            start = datetime(year=time_now.year, month=time_now.month, day=time_now.day, hour=16, minute=56)
            end = datetime(year=time_now.year, month=time_now.month, day=time_now.day, hour=20, minute=55)

    return start, end


print(get_time_period())