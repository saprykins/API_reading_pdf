#!/usr/bin/env python

"Initialization of WSGI application"

from flaskr.__init__ import init_app

app = init_app()

if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
