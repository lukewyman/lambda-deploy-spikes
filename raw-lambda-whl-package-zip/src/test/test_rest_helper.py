import pytest
from rest_helper.rest_helper import post, get

def test_post():
    response = post('https://httpbin.org/post', {'key':'value'})

    assert response.status_code == 200


def test_get():
    response = get('https://httpbin.org/get')

    assert response.status_code == 200