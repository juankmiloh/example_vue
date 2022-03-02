import datetime
from flask import abort
from ..util import constants 

def to_date(date):
    try:
        return datetime.datetime.strptime(date, constants.BASIC_DATE_FORMAT).date()
    except Exception as e: 
        print(e)
        abort(400)

def add_wrapper(data):
    return {'items': data, 'total': len(data)}

def get_last_month(delay):
    today = datetime.date.today() - datetime.timedelta(days=delay)
    first = today.replace(day=1)
    return first - datetime.timedelta(days=1)

def to_bool(bool):
    return True if bool == 'true' else False