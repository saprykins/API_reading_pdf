import json
from model import generate_file_id, save_metadata_and_text_to_data_base, save_received_pdf
from flask import Blueprint
from model import Pdf

from model import session
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
    init_db()
    record_id = save_metadata_and_text_to_data_base(file_id)

    # doc_id in Python dictionary
    doc_id_dictionary = {"id": record_id}

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

    # search by record_id in database works, but only once
    record_id = id

    pdf_item = session.query(Pdf).filter_by(id=record_id).first()

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

    file_information_in_json = json.dumps(meta_data_dictionary)

    return file_information_in_json

# routing to the endpoint that prints out the text from text-file
# the followting commmand can be used to check the display
# curl -s http://localhost:5000/text/document_id.txt


@get_text_blueprint.route('/text/<id>.txt', methods=['GET', 'POST'])
def print_text(id):
    file_id = id

    # convert into JSON:

    pdf_item = session.query(Pdf).filter_by(id=file_id).first()
    doc_text_in_dict = {'text': pdf_item.text}
    doc_text_in_json = json.dumps(doc_text_in_dict)

    return doc_text_in_json
