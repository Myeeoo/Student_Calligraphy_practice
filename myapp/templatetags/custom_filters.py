from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def time_since_checkin(checkin_date):
    
    now = datetime.now()
    checkin_datetime = datetime.strptime(checkin_date, "%Y-%m-%d %H:%M:%S")
    time_since = now - checkin_datetime
    
    if time_since < timedelta(minutes=1):
        return "刚刚"
    elif time_since < timedelta(hours=1):
        return str(int(time_since.seconds / 60)) + "分钟前"
    elif time_since < timedelta(days=1):
        return str(int(time_since.seconds / 3600)) + "小时前"
    else:
        return checkin_datetime.strftime("%Y-%m-%d")
