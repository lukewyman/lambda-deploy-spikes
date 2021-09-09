from rest_heler.rest_helper import post

def handler(event, context):
    response = post('https://httpbin.org/post', {'key':'value'})
    print(response.text)
    return response.text