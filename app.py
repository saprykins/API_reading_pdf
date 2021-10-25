from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename


# requirements related to controller are to accomplish:
# 1/ must return file_id, not filename
# 2/ to test in virtual environment

# requirements related to view are to accomplish:
# 1/ prints out all the text, not only the first line
# 2/ must find the file by id, not its name

# possible improuvements:
# 1/ check file extention before upload
# 2/ delete "debug=True" in main function
# 3/ locally saved file-names must be dynamic



# CONTROLLER

# initialization of WSGI application
app = Flask(__name__)


# routing to index page
@app.route("/")
def index():
    return str("Index page")


# routing to the endpoint that allows file upload
@app.route('/documents', methods=['POST'])
def upload_file():
    """
    It saves the file in "local_file_path" received in curl command 
    and returns file's name
    
    An example of curl command to upload a file from command line:
    curl -F file=@"f.txt" http://localhost:5000/documents
    """
    local_file_path = '../DOWNLOADS/uploaded_file-3.txt'
    file = request.files['file']
    file.save(local_file_path)
    filename=secure_filename(file.filename)   
    return filename



# VIEW

# describes document processing state, metadata and shares a link to its content
# @app.route("/documents/<id>")


# displays the extracted text
@app.route('/text/<id>.txt', methods=['GET', 'POST'])
def print_text(id):
    file_path = '../DOWNLOADS/'
    # id = 'uploaded_file-3'
    file_name = id
    file_path = file_path + file_name + '.txt'
    
    with open(file_path) as feed:
        for line in feed:
            # returns only the first line
            return str(line.strip())



# MODEL

# extracting metadata from pdf-file
# extracting text from pdf-file


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()





