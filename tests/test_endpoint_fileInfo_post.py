# i didn't put error 405, 
# need to check if a sent file is wrong

from flaskr.__init__ import init_app

def test_upload_check_get():
    """
    GIVEN a Flask application
    WHEN the '/' page is requested(POST)
    THEN check that the HTTP response is 405
    """
    flask_app = init_app()
    # flask_app = init_app('flask_test.cfg')
    with flask_app.test_client() as test_client:
        response = test_client.post("/documents/<id>")
        assert response.status_code == 405
        