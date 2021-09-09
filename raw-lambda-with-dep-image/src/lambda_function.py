import requests

def handler(event, context):
    response = requests.get('https://www.test.com')
    print(response.text)
    return response.text

if __name__ == '__main__':
    handler('', '')