#!/usr/bin/env python

'''
Tests of index page
'''

from wsgi import init_app
from test_app import client

'''
def test_index_post_get():
    """
    GIVEN a Flask application
    a)
    WHEN the '/' page is requested(POST)
    THEN check that the HTTP response is 405
    b)
    WHEN the '/' page is requested(GET)
    THEN check that the HTTP response is 200
    """

    flask_app = init_app()
    # part a)
    with flask_app.test_client() as test_client:
        response = test_client.post('/')
        assert response.status_code == 405
    
    # part b)
    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
'''

def test_index_page(client):
    """
    GIVEN a Flask application
    a)
    WHEN the '/' page is requested(GET)
    THEN check that the HTTP response is 200
    b)
    THEN check that the text contains 'Index page'
    c)
    WHEN the '/' page is requested(POST)
    THEN check that the HTTP response is 405
    """

    # send HTTP get request to index page
    response = client.get('/')
    # part a)
    assert response.status_code == 200

    # part b)
    assert b'Index page' in response.data

    # part c)
    response = client.post('/')
    assert response.status_code == 405
