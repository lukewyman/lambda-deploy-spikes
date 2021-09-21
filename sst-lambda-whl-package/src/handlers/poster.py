from rest_helper.rest_helper import post
from dates_magic.pretty_datetime import get_pretty_now

def handler(event, context):
    response = {}
    response['pretty_date_time'] = get_pretty_now()
    response['httpbin_response'] = post('https://httpbin.org/post', {'key':'value'})

    print(response)

    return response