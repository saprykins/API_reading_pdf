import json
from model import generate_file_id, save_metadata_and_text_to_data_base, save_received_pdf
from model import extract_metadata_from_pdf, get_doc_text_in_dictionary
from flask import Blueprint
from model import Pdf

# from database import Base
from sqlalchemy import Column, Integer, String
from model import session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from model import init_db

index_blueprint = Blueprint('index', __name__)
upload_file_blueprint = Blueprint('upload_file', __name__)
get_file_info_blueprint = Blueprint('get_file_info', __name__)
get_text_blueprint = Blueprint('get_text', __name__)

# routing to index page


@index_blueprint.route("/")
def index():
    return str("Index page")

# routing to the endpoint that allows file upload


@upload_file_blueprint.route('/documents', methods=['POST'])
def upload_file():
    '''
    It saves the file in "local_file_path" received in curl command 
    and returns file's name
    An example of curl command to upload a file from command line:
    curl -sF file=@"sample.pdf" http://localhost:5000/documents
    '''

    file_id = generate_file_id()

    save_received_pdf(file_id)
    # record_id_in_db = save_metadata_and_text_to_data_base(file_id)

    # Base.query = session.query_property()
    init_db()
    # file_id = r'C:\_My_Files\_FA\_ETUDES\Python\py-code\flask_reading_pdf_try_to_put_views_aside\uploads\carhovchadjijffq.pdf'
    # file_id = 'carhovchadjijffq'
    save_metadata_and_text_to_data_base(file_id)

    # doc_id in Python dictionary
    doc_id_dictionary = {"id": file_id, }

    # convert into JSON:
    doc_id_in_json = json.dumps(doc_id_dictionary)
    return doc_id_in_json

# routing to the endpoint that describes document's processing state
# shares metadata and links to file's content
# curl -s http://localhost:5000/documents/document_ic


@get_file_info_blueprint.route("/documents/<id>", methods=['GET', 'POST'])
def processing_meta_link(id):
    '''
    It displays the link to the file
    '''

    # file_id = id
    file_id = 1
    '''
    # get dictionary that holds meta-data
    meta_data_dictionary = extract_metadata_from_pdf(file_id)
    # our_pdf = session.query(Pdf).filter_by(id=file_id).first()
    
    # our_pdf.creation_date

    # return file_path_link
    # file_path_link = 'http://localhost:5000/text/' + file_id + '_text.txt'
    # meta_link = 'http://localhost:5000/text/' + file_id + '_meta.txt'

    # add to dictionary status, links to file with text and meta-data
    meta_data_dictionary['status'] = 'succes'
    # meta_data_dictionary['link_to_meta_data_file'] = meta_link
    # meta_data_dictionary['link_to_file_with_text'] = file_path_link
    '''
    pdf_item = session.query(Pdf).filter_by(id=file_id).first()

    meta_data_dictionary = {}
    meta_data_dictionary['author'] = pdf_item.author
    meta_data_dictionary['creation_date'] = pdf_item.creation_date
    meta_data_dictionary['modification_date'] = pdf_item.modification_date

    meta_data_dictionary['creator'] = pdf_item.creator
    meta_data_dictionary['status'] = pdf_item.status
    meta_data_dictionary['text'] = pdf_item.text
    meta_data_dictionary['file_id'] = pdf_item.file_id

    file_information_in_json = json.dumps(meta_data_dictionary)

    return file_information_in_json

# routing to the endpoint that prints out the text from text-file
# the followting commmand can be used to check the display
# curl -s http://localhost:5000/text/document_id.txt


@get_text_blueprint.route('/text/<id>.txt', methods=['GET', 'POST'])
def print_text(id):
    # file_id = id
    file_id = 1

    # convert into JSON:
    # doc_text_in_json = json.dumps(get_doc_text_in_dictionary(file_id))
    pdf_item = session.query(Pdf).filter_by(id=file_id).first()
    doc_text_in_json = pdf_item.text
    return doc_text_in_json
