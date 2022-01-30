#!/usr/bin/env python

"""
Tests endpoints: 
1/ to send files ('/documents')
2/ to retrieve information ('/documents/<id>' and '/text/<id>')
"""

from wsgi import init_app

from test_app import client


def test_endpoint_documents_errors():
    """
    GIVEN a Flask application
    a)
    WHEN the '/documents/<id>' page is requested(GET)
    THEN check that the HTTP response is 404
    b)
    WHEN the '/documents/<id>' page is requested(POST)
    THEN check that the HTTP response is 405
    """

    flask_app = init_app()

    with flask_app.test_client() as test_client:
        # part a)
        response = test_client.get("/documents/100")
        assert response.status_code == 404

        # part b)
        response = test_client.post("/documents/1")
        assert response.status_code == 405


def test_endpoint_documents_pdf_document(client):
    """
    GIVEN a Flask application and pdf-file
    WHEN the '/documents' page is requested(POST)
    THEN check that the HTTP response is 200
    """
    data = dict()
    data["file"] = open("./sample.pdf", "rb")
    response = client.post("/documents", data=data, follow_redirects=True)
    assert response.status_code == 200


def test_endpoint_documents_non_pdf_document(client):
    """
    GIVEN a Flask application and NON pdf-file
    WHEN the '/documents' page is requested(POST)
    THEN check that the HTTP response is 415
    """
    data = dict()
    data["file"] = open("./requirements.txt", "rb")
    response = client.post("/documents", data=data, follow_redirects=True)
    assert response.status_code == 415


def test_get_existing_documents():
    """
    GIVEN a Flask application
    WHEN the '/documents/<id>' page is requested(GET)
    THEN check that the HTTP response is 200
    """
    flask_app = init_app()
    with flask_app.test_client() as test_client:
        response = test_client.get("/documents/1")
        assert response.status_code == 200


def test_get_text(client):
    """
    GIVEN a Flask application
    a)
    WHEN the '/text/<id>' existing page is requested(GET)
    THEN check that the HTTP response is 200
    b)
    WHEN the '/text/<id>' NON existing page is requested(GET)
    THEN check that the HTTP response is 404
    """
    # part a
    response = client.get("/text/1.txt")
    assert response.status_code == 200

    # part b
    response = client.get("/text/100.txt")
    assert response.status_code == 404
