import os
import tempfile
import io
# from flask import url_for
import pytest

from flaskr.__init__ import init_app
from flaskr.model import init_db


# configuration of application for testing
@pytest.fixture
def client():
    # create data file and name
    db_fd, db_path = tempfile.mkstemp()
    
    # activate 'tesing' flag
    app = init_app({'TESTING': True, 'DATABASE': db_path})

    # initialization of a new database
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client
    
    # close the database file
    os.close(db_fd)
    os.unlink(db_path)


def test_empty_db(client):
    """
    Check that index page text has 'Index page' text in it
    """
    # send HTTP get request to index page
    rv = client.get('/')
    assert b'Index page' in rv.data

    """
    Check that index page text has 'Index page' text in it
    """    
    # os.remove('db_path')

    flask_app = init_app()
    with flask_app.test_client() as test_client:
        response = test_client.get("/documents/1")
        assert response.status_code == 404

    with flask_app.test_client() as test_client:
        response = test_client.get('/text/1.txt')
        assert response.status_code == 404
    

def test_upload_check_get_NOK():
    """
    GIVEN a Flask application
    WHEN the '/documents/<id>' page is requested(POST)
    THEN check that the HTTP response is 405
    """
    flask_app = init_app()
    
    with flask_app.test_client() as test_client:
        response = test_client.get("/documents/100")
        assert response.status_code == 404
        
        response = test_client.post("/documents/1")
        assert response.status_code == 405

        
def test_send_document(client):
    """
    Test that sending a document is possible
    """

    data = dict()
    data['file'] = open('./sample.pdf', 'rb')
    response = client.post('/documents', data=data, follow_redirects=True)
    assert response.status_code == 200
    
    data['file'] = open('./requirements.txt', 'rb')
    response = client.post('/documents', data=data, follow_redirects=True)
    assert response.status_code == 415


def test_upload_check_get():
    """
    GIVEN a Flask application
    WHEN the '/documents' page is requested(POST)
    THEN check that the HTTP response is 400
    """
    flask_app = init_app()
    with flask_app.test_client() as test_client:
        data = {}
        response = test_client.post("/documents", data=data, content_type="multipart/form-data")
        assert response.status_code == 400


def test_upload_check_get_OK():
    """
    GIVEN a Flask application
    WHEN the '/documents/<id>' page is requested(POST)
    THEN check that the HTTP response is 405
    """
    flask_app = init_app()
    with flask_app.test_client() as test_client:
        response = test_client.get("/documents/1")
        assert response.status_code == 200


def test_get_text(client):
    # Check existing record from database
    response = client.get('/text/1.txt')
    assert response.status_code == 200

    # Check NON existing record from database
    response = client.get('/text/100.txt')
    assert response.status_code == 404