from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename



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

        
if __name__ == '__main__':
    app.run(debug=True)


# MODEL

# extracting metadata from pdf-file
# extracting text from pdf-file


# VIEW

# describes document processing state, metadata and shares a link to its content
# @app.route("/documents/<id>")

# displays the extracted text
# @app.route("/text/<id>.txt")

