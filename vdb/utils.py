import datetime


def get_current_quarter():
    current_month = datetime.datetime.now().month
    if current_month in range(1, 4):
        return 1
    elif current_month in range(4, 7):
        return 2
    elif current_month in range(7, 10):
        return 3
    else:
        return 4
    

def get_current_year():
    year = datetime.datetime.now().year

    return [year, get_current_quarter()]
