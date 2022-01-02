# from flaskr.controller import upload_file
from flaskr.__init__ import init_app

def test_index_check_post():
    """
    GIVEN a Flask application
    WHEN the '/' page is requested(POST)
    THEN check that the HTTP response is 405
    """
    flask_app = init_app()
    with flask_app.test_client() as test_client:
        response = test_client.post('/')
        assert response.status_code == 405