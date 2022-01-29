from wsgi import init_app

def test_index_check_post():
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


def test_empty_db(client):
    """
    Check that index page text has 'Index page' text in it
    """
    # send HTTP get request to index page
    rv = client.get('/')
    assert b'Index page' in rv.data
    