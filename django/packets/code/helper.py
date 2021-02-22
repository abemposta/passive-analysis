from django import template
from datetime import datetime, timedelta

def template_exists(value):
    try:
        template.loader.get_template(value)
        return True
    except template.TemplateDoesNotExist:
        return False

def get_page(req):
    if (not req):
        return None
    try:
        page = int(req['page'])
        return page
    except ValueError as e:
        print("ERROR: page must be int. ", e)
        return None

def get_date_interval(req):
    if (not req):
        return None
    dates = {}
    inidate = req['start-time']
    enddate = req['end-time']
    try:
        inidateo = datetime.strptime(inidate, '%Y-%m-%dT%H:%M')
        enddateo = datetime.strptime(enddate, '%Y-%m-%dT%H:%M')
    except Exception as e:
        return None
    if (enddate <= inidate):
        return None
    dates["inidate"] = inidate
    dates["enddate"] = enddate
    return dates

def get_day(req):
    interval = {}
    if req:
        statsday = req['day']
        try:
            statsdayo = datetime.strptime(statsday, '%Y-%m-%d')
        except ValueError:
            return None
    else:
        return None
    endtime = statsdayo + timedelta(days=1)
    interval["ini"] = statsday
    interval["end"] = endtime.strftime("%Y-%m-%d")

    return interval
