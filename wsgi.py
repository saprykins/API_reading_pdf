from flaskr.__init__ import init_app

# initialization of WSGI application
app = init_app()

if __name__ == '__main__':
    # app.run(debug=True)
    app.run()