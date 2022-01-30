#!/usr/bin/env python

"""
Client configuration for tests
"""

import os
import tempfile

import pytest
from flaskr.__init__ import init_app
from flaskr.model import init_db


# configuration of application for testing
@pytest.fixture
def client():
    # create data file and name
    db_fd, db_path = tempfile.mkstemp()

    # activate 'tesing' flag
    app = init_app({"TESTING": True, "DATABASE": db_path})

    # initialization of a new database
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    # close the database file
    os.close(db_fd)
    os.unlink(db_path)
