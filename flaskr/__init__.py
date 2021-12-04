# STEPS OF IMPROUVEMENT
# Try to use pprint
# Point to improuve: if file name is the same as existing, get a msg
# delete "debug=True" in main function
# need to add processing state (to be able to share status)
# work with exceptions
# charge out views.py // probably need to move instructions to controller
# add raise exception capture when no db-file and you try to get data
# tbc number of blueprints
# tbc if can keep app in __init__.py outside function



from flask import Flask
from controller import index_blueprint, upload_file_blueprint, get_file_info_blueprint, get_text_blueprint

# initialization of WSGI application
app = Flask(__name__)

app.register_blueprint(index_blueprint)
app.register_blueprint(upload_file_blueprint)
app.register_blueprint(get_file_info_blueprint)
app.register_blueprint(get_text_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
