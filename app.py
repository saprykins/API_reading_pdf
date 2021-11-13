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

# return json
import json


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
# temporary_pdf_file_name = 'temporary_file'


def generate_file_id():
    file_id = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    return str(file_id)


# below is temporary solution
# it is used to check pdf data and text exctraction to local text files
def save_metadata_and_text_from_pdf_to_text_files(doc_id):
    path_to_text_result = path_to_save_folder + doc_id + '_text.txt'
    path_to_meta_result = path_to_save_folder + doc_id + '_meta.txt'

    with open(path_to_text_result, 'w', encoding='utf-8') as f:
        f.write(extract_text_from_pdf(doc_id))

    with open(path_to_meta_result, 'w', encoding='utf-8') as f:
        for items in extract_metadata_from_pdf(doc_id):
            f.write(items)


# CONTROLLER
# initialization of WSGI application
app = Flask(__name__)


# routing to index page
@app.route("/")
def index():
    return str("Index page")


def convert_doc_id_into_json(doc_id):

    # doc_id in Python dictionary
    doc_id_dictionary = {"id": doc_id, }

    # convert into JSON:
    doc_id_in_json = json.dumps(doc_id_dictionary)
    return doc_id_in_json


"""
def convert_doc_text_into_json(doc_id):
    
    # doc_id in Python dictionary
    doc_text_in_dictionary = {"text": doc_id, }

    # convert into JSON:
    doc_text_in_json = json.dumps(doc_text_in_dictionary)
    return doc_text_in_json
"""

# routing to the endpoint that allows file upload


@app.route('/documents', methods=['POST'])
def upload_file():
    '''
    It saves the file in "local_file_path" received in curl command 
    and returns file's name

    An example of curl command to upload a file from command line:
    curl -sF file=@"1.pdf" http://localhost:5000/documents
    '''

    file_id = generate_file_id()

    local_file_path = path_to_save_folder + file_id + '.pdf'
    file = request.files['file']
    file.save(local_file_path)
    # filename = secure_filename(file.filename)

    save_metadata_and_text_from_pdf_to_text_files(file_id)
    return convert_doc_id_into_json(file_id)


# extracting text from pdf-file
def extract_text_from_pdf(doc_id):
    path_to_pdf = path_to_save_folder + doc_id + '.pdf'
    text = extract_text(path_to_pdf)
    return text


# extracting metadata from pdf-file
# returns dictionary
def extract_metadata_from_pdf(doc_id):
    path_to_pdf = path_to_save_folder + doc_id + '.pdf'
    with open(path_to_pdf, 'rb') as file:
        parser = PDFParser(file)
        doc = PDFDocument(parser)

        # converting data to json format
        meta_data = {}
        for item in doc.info:
            meta_data['author'] = item['Producer'].decode("utf-8", 'ignore')
            meta_data['creation_date'] = item['CreationDate'].decode(
                "utf-8", 'ignore')
            meta_data['modification_date'] = item['ModDate'].decode(
                "utf-8", 'ignore')
            meta_data['creator'] = item['Creator'].decode("utf-8", 'ignore')
            # meta_data['title'] = item['Title'].decode("utf-8", 'ignore')
        return meta_data


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

    # get dictionary of meta-data
    meta_data_dictionary = extract_metadata_from_pdf(file_id)


#     message = 'to display the text from pdf type copy the link below'
    file_path_link = 'http://localhost:5000/text/' + file_id + '_text.txt'
    meta_link = 'http://localhost:5000/text/' + file_id + '_meta.txt'
    # return file_path_link

    # adding more elements to dictionary
    meta_data_dictionary['status'] = 'succes'
    meta_data_dictionary['link_to_meta_data_file'] = meta_link
    meta_data_dictionary['link_to_file_with_text'] = file_path_link

    file_information_in_json = json.dumps(meta_data_dictionary)

    return file_information_in_json


# routing to the endpoint that prints out the text from text-file
# the followting commmand can be used to check the display
# curl -s http://localhost:5000/text/xyz.txt
@app.route('/text/<id>.txt', methods=['GET', 'POST'])
def print_text(id):
    file_name = id
    file_path = path_to_save_folder + id + '_text.txt'

    with open(file_path) as feed:
        text = feed.read()

        # doc_id in Python dictionary
        doc_text_in_dictionary = {"text": text, }

        # convert into JSON:
        doc_text_in_json = json.dumps(doc_text_in_dictionary)

        return doc_text_in_json


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
