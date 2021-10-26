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

# need to add processing state




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
    curl -sF file=@"f.txt" http://localhost:5000/documents
    """
    local_file_path = '../DOWNLOADS/uploaded_file-3.txt'
    file = request.files['file']
    file.save(local_file_path)
    filename=secure_filename(file.filename)   
    return filename



# VIEW

# routing to the endpoint that describes document's processing state
# shares metadata and links to file's content

@app.route("/documents/<id>", methods=['GET', 'POST'])
def processing_meta_link(id):
    """
    It shares the link to the file
    """
    # file_path = '../DOWNLOADS/'
    # id = 'uploaded_file-3'
    file_id = id
    message = 'to display the text from pdf type copy the link below'
    file_path_link = 'http://localhost:5000/text/' + file_id + '.txt'
    return file_path_link


# routing to the endpoint that prints out the text from text-file
# the followting commmand can be used to check the display
# curl -s http://localhost:5000/text/uploaded_file-3.txt
@app.route('/text/<id>.txt', methods=['GET', 'POST'])
def print_text(id):
    file_path = '../DOWNLOADS/'
    # id = 'uploaded_file-3'
    file_name = id
    file_path = file_path + file_name + '.txt'
    
    with open(file_path) as feed:
        data = feed.read()
        return str(data)



# MODEL

# extracting metadata from pdf-file
# extracting text from pdf-file


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
