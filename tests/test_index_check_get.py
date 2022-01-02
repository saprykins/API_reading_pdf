# from flaskr.controller import upload_file
from flaskr.__init__ import init_app

def test_index_check_get():
    """
    GIVEN a Flask application
    WHEN the '/' page is requested(GET)
    THEN check that the HTTP response is 200
    """
    flask_app = init_app()
    # flask_app = init_app('flask_test.cfg')
    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b"Index page" in response.data