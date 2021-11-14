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

# Point to improuve: if file name is the same as existing, get a msg
# to test in virtual environment
# check file extention before upload (pdf only)
# delete "debug=True" in main function
# need to add processing state (to be able to share status)
# for docs, you can include advice to use gitk ou git log --graph to show commits


# MODEL

# global attributes
path_to_save_folder = '../PROJECT/'


def generate_file_id():
    file_id = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    return str(file_id)


# saves meta-data and text from pdf to local text files
def save_metadata_and_text_from_pdf_to_text_files(doc_id):
    path_to_text_result = path_to_save_folder + doc_id + '_text.txt'
    path_to_meta_result = path_to_save_folder + doc_id + '_meta.txt'

    with open(path_to_text_result, 'w', encoding='utf-8') as f:
        f.write(extract_text_from_pdf(doc_id))

    with open(path_to_meta_result, 'w', encoding='utf-8') as f:
        f.write(json.dumps(extract_metadata_from_pdf(doc_id)))


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


# routing to the endpoint that allows file upload
@app.route('/documents', methods=['POST'])
def upload_file():
    '''
    It saves the file in "local_file_path" received in curl command 
    and returns file's name

    An example of curl command to upload a file from command line:
    curl -sF file=@"sample_file_to_upload.pdf" http://localhost:5000/documents
    '''

    file_id = generate_file_id()

    local_file_path = path_to_save_folder + file_id + '.pdf'
    file = request.files['file']
    file.save(local_file_path)
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
# curl -s http://localhost:5000/documents/document_ic
@app.route("/documents/<id>", methods=['GET', 'POST'])
def processing_meta_link(id):
    """
    It displays the link to the file
    """

    file_id = id

    # get dictionary that holds meta-data
    meta_data_dictionary = extract_metadata_from_pdf(file_id)

    file_path_link = 'http://localhost:5000/text/' + file_id + '_text.txt'
    meta_link = 'http://localhost:5000/text/' + file_id + '_meta.txt'
    # return file_path_link

    # adds to dictionary status, links to file with text and meta-data
    meta_data_dictionary['status'] = 'succes'
    meta_data_dictionary['link_to_meta_data_file'] = meta_link
    meta_data_dictionary['link_to_file_with_text'] = file_path_link

    file_information_in_json = json.dumps(meta_data_dictionary)

    return file_information_in_json


# routing to the endpoint that prints out the text from text-file
# the followting commmand can be used to check the display
# curl -s http://localhost:5000/text/document_id.txt
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
