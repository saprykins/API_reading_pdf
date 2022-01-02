#!/usr/bin/env python

"Controller module that describes endpoints and its functions"

# import json
from flask import jsonify
from flask import Blueprint

# to check uploaded file-name
from flask import request
from werkzeug.utils import secure_filename

from flaskr.model import generate_file_id, save_metadata_and_text_to_data_base
from flaskr.model import save_received_pdf, Pdf, session, init_db, id_in_database
# from model import Pdf
# from model import session
# from model import init_db
# from model import id_in_database


# blueprints used to split code into several files
index_blueprint = Blueprint('index', __name__)
upload_file_blueprint = Blueprint('upload_file', __name__)
get_file_info_blueprint = Blueprint('get_file_info', __name__)
get_text_blueprint = Blueprint('get_text', __name__)


@index_blueprint.route("/")
def index():
    """
    routing to sample index page http://localhost:5000/
    """
    return str("Index page")


@upload_file_blueprint.route('/documents', methods=['POST'])
def upload_file():
# def upload_file():
    '''
    Routing to the endpoint that allows file upload
    It saves the uploaded file on local machine and returns file's id
    '''

    # must add extra code to check if there's a file
    file = request.files['file']
    """
    # it's a problem for pylint
    if request.method == "POST":
        # check if the post request has the file part
        # tbc below code
        if "file" not in request.files:
            error_msg = {
                "error_message":"no file chosen",
                }
            return jsonify(error_msg)


    # verification if filename is empty
    if file.filename == "":
        error_msg = {
            "error_message":"no file chosen",
            }
        return jsonify(error_msg)
    """

    # verification of file type from its name
    filename = secure_filename(file.filename)

    # only pdf- and PDF-files are allowed
    file_extention = filename[-3::].lower()

    # if file is pdf-type
    # it saves the file and returns its identifier from database in json-format
    if file_extention == 'pdf':
        file_id = generate_file_id()
        save_received_pdf(file_id)
        init_db()
        record_id = save_metadata_and_text_to_data_base(file_id)

        # put doc_id in Python dictionary
        doc_id_dictionary = {"id": record_id}
        return jsonify(doc_id_dictionary)

    # in case the file is not pdf
    # it returns error in json and 415 HTML error code (Unsupported Media Type)

    error_msg = {
        "error_message":"only .pdf or .PDF-file types are allowed",
        }
    return jsonify(error_msg), 415



@get_file_info_blueprint.route("/documents/<document_id>", methods=['GET'])
def processing_meta_link(document_id):
    '''
    Routing to the endpoint that returns document's metadata in json
    id is id in database
    '''

    if id_in_database(document_id):
        pdf_item = session.query(Pdf).filter_by(id=document_id).first()
        meta_data_dictionary = {}
        meta_data_dictionary['author'] = pdf_item.author
        meta_data_dictionary['creation_date'] = pdf_item.creation_date
        meta_data_dictionary['modification_date'] = pdf_item.modification_date

        meta_data_dictionary['creator'] = pdf_item.creator
        meta_data_dictionary['status'] = pdf_item.status
        # meta_data_dictionary['text'] = pdf_item.text
        meta_data_dictionary['file_id'] = pdf_item.file_id
        meta_data_dictionary['link_to_content'] = 'http://localhost:5000/text/' + \
            str(pdf_item.id) + '.txt'
        return jsonify(meta_data_dictionary)

    # in other case it returns error message in json and 404 HTML error code (Not Found)

    error_msg = {
        "error_message":"the id you ask does not exist",
        }
    return jsonify(error_msg), 404


@get_text_blueprint.route('/text/<document_id>.txt', methods=['GET'])
def print_text(document_id):
    """
    Routing to the endpoint that returns related text from database
    """
    # checks if requested id in database
    # and returns from database the text in json-format
    if id_in_database(document_id):
        pdf_item = session.query(Pdf).filter_by(id=document_id).first()
        doc_text_in_dict = {'text': pdf_item.text}
        return jsonify(doc_text_in_dict)

    # in other case it returns error message in json and 404 HTML error code (Not Found)
    error_msg = {
        "error_message":"the id you ask does not exist",
        }
    return jsonify(error_msg), 404
