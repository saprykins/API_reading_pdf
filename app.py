# working with web
from flask import Flask
from flask import render_template
from flask import request
# from werkzeug.utils import secure_filename


# reading from pdf
from pdfminer.high_level import extract_text


# extracting data from pdf
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import pprint

# file-id generator
import random
import string


# STEPS OF IMPROUVEMENT

# requirements related to controller are to accomplish:
# 1/ must return file_id, not filename
# -- Point to improuve: if file name is the same as existing, get a msg
# -- several points are not allowed in file-names (only pdf are allowed)
# 2/ to test in virtual environment

# requirements related to view are to accomplish:
# 1/ prints out all the text, not only the first line
# 2/ must find the file by id, not its name

# possible improuvements:
# 1/ check file extention before upload (pdf only)
# 2/ delete "debug=True" in main function

# need to add processing state (to be able to share status)
# metadata from pdf-files is flatten to be saved to text files
# the issue should changed when using database

# global atributes to be handed over via functions
# for docs, you can include advice to use gitk ou git log --graph to show commits


# MODEL
# working with database

# global attributes
path_to_save_folder = '../PROJECT/'

# temporary pdf-file is saved in case issues during text extraction
temporary_pdf_file_name = 'temporary_file'


def generate_file_id():
    file_id = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    return str(file_id)


# below is temporary solution
# it is used to check pdf data and text exctraction to local text files
def save_metadata_and_text_from_pdf_to_text_files(id):
    path_to_text_result = path_to_save_folder + id + '_text.txt'
    path_to_meta_result = path_to_save_folder + id + '_meta.txt'

    with open(path_to_text_result, 'w', encoding='utf-8') as f:
        f.write(extract_text_from_pdf())

    with open(path_to_meta_result, 'w', encoding='utf-8') as f:
        for items in extract_metadata_from_pdf():
            f.write(items)


# CONTROLLER
# initialization of WSGI application
app = Flask(__name__)


# routing to index page
@app.route("/")
def index():
    return str("Index page")


# working version
# routing to the endpoint that allows file upload
@app.route('/documents', methods=['POST'])
def upload_file():
    '''
    It saves the file in "local_file_path" received in curl command 
    and returns file's name

    An example of curl command to upload a file from command line:
    curl -sF file=@"1.pdf" http://localhost:5000/documents
    '''

    local_file_path = path_to_save_folder + temporary_pdf_file_name + '.pdf'
    file = request.files['file']
    file.save(local_file_path)
    # filename = secure_filename(file.filename)

    file_id = generate_file_id()
    save_metadata_and_text_from_pdf_to_text_files(file_id)
    return file_id


# extracting text from pdf-file
def extract_text_from_pdf():
    path_to_sample_pdf = path_to_save_folder + temporary_pdf_file_name + '.pdf'
    text = extract_text(path_to_sample_pdf)
    return text


# extracting metadata from pdf-file
def extract_metadata_from_pdf():
    path_to_sample_pdf = path_to_save_folder + temporary_pdf_file_name + '.pdf'
    with open(path_to_sample_pdf, 'rb') as file:
        parser = PDFParser(file)
        doc = PDFDocument(parser)
    # next there're 2 options:
    # 1/ work with a list of dictionaries (difficult to write in a text file) or
    # 2/ flatten (easy to write in file)

    # so, below are 2 options (is kept to use when working with database):
    # 1/ return doc.info
    # 2/ option:
    array = []
    for items in doc.info:
        array.append(str(items))
    return array


# VIEW

# routing to the endpoint that describes document's processing state
# shares metadata and links to file's content
# curl -s http://localhost:5000/documents/xyz
@app.route("/documents/<id>", methods=['GET', 'POST'])
def processing_meta_link(id):
    """
    It displays the link to the file
    """

    file_id = id
    message = 'to display the text from pdf type copy the link below'
    file_path_link = 'http://localhost:5000/text/' + file_id + '_text.txt'
    meta_link = 'http://localhost:5000/text/' + file_id + '_meta.txt'
    # return file_path_link

    # below i try to put several things in return statement
    # it should be replaced working with MVC-model
    status = 'document is successfully saved'
    msg_meta = 'below is the link to meta data'
    msg_text = 'below is the link to text'
    new_line = '\n'
    status_metadata_link = (
        status + new_line + msg_meta + new_line + meta_link + new_line +
        msg_text + new_line + file_path_link)
    return status_metadata_link


# routing to the endpoint that prints out the text from text-file
# the followting commmand can be used to check the display
# curl -s http://localhost:5000/text/xyz.txt
@app.route('/text/<id>.txt', methods=['GET', 'POST'])
def print_text(id):
    file_name = id
    file_path = path_to_save_folder + id + '_text.txt'

    with open(file_path) as feed:
        data = feed.read()
        return str(data)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
