from datetime import datetime
import pytz

def get_pretty_now():
    return datetime.utcnow().strftime('%B %d, %Y at %I:%M %p')