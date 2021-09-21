from rest_helper.rest_helper import get
from dates_magic.pretty_datetime import get_pretty_now

def handler(event, context):
    response = {}
    response['pretty_date_time'] = get_pretty_now()
    response['httpbin_response'] = get('https://httpbin.org/get')

    print(response)

    return response