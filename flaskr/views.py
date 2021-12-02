import json
from flask import Blueprint

# to check uploaded file-name
from flask import request
from werkzeug.utils import secure_filename

from model import generate_file_id, save_metadata_and_text_to_data_base, save_received_pdf
from model import Pdf
from model import session
from model import init_db



# blueprints used to split code into several files 
index_blueprint = Blueprint('index', __name__)
upload_file_blueprint = Blueprint('upload_file', __name__)
get_file_info_blueprint = Blueprint('get_file_info', __name__)
get_text_blueprint = Blueprint('get_text', __name__)


@index_blueprint.route("/")
def index():
    """
    routing to index page http://localhost:5000/
    """
    return str("Index page")


@upload_file_blueprint.route('/documents', methods=['POST'])
def upload_file():
    '''
    Routing to the endpoint that allows file upload
    It saves the uploaded file on local machine and returns file's id
    '''
    
    # checks received file extention
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_extention = filename[-3::]
    if file_extention == 'pdf': 
        file_id = generate_file_id()
        save_received_pdf(file_id)
        init_db()
        record_id = save_metadata_and_text_to_data_base(file_id)

        # put doc_id in Python dictionary
        doc_id_dictionary = {"id": record_id}

        # convert dictionary into JSON format
        doc_id_in_json = json.dumps(doc_id_dictionary)
        return doc_id_in_json
    else:
        error_msg = {
            # "status":500,
            "error_message":"the file-type you send is not pdf",
            }
        return error_msg



@get_file_info_blueprint.route("/documents/<id>", methods=['GET', 'POST'])
def processing_meta_link(id):
    '''
    Routing to the endpoint that returns document's metadata in json
    '''
    
    # gets id from the endpoint above
    record_id = id

    # retrives information from database to dictionary format
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




@get_text_blueprint.route('/text/<id>.txt', methods=['GET', 'POST'])
def print_text(id):
    """
    Routing to the endpoint that returns related text from database
    """
    pdf_item = session.query(Pdf).filter_by(id=id).first()
    doc_text_in_dict = {'text': pdf_item.text}
    doc_text_in_json = json.dumps(doc_text_in_dict)

    return doc_text_in_json
