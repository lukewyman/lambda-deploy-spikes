from rest_helper.rest_helper import get 

def handler(event, context):
    response = get('https://httpbin.org/get')
    print(response.text)
    return response.text