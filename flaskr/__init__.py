from flask import Flask
from views import index_blueprint, upload_file_blueprint, get_file_info_blueprint, get_text_blueprint


# initialization of WSGI application
app = Flask(__name__)

app.register_blueprint(index_blueprint)
app.register_blueprint(upload_file_blueprint)
app.register_blueprint(get_file_info_blueprint)
app.register_blueprint(get_text_blueprint)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
