import requests

def post(url, body):
    return requests.post(url, body)


def get(url):
    return requests.get(url)