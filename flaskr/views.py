# import json
from flask import jsonify
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
    routing to sample index page http://localhost:5000/
    """
    return str("Index page")


@upload_file_blueprint.route('/documents', methods=['POST'])
def upload_file():
    '''
    Routing to the endpoint that allows file upload
    It saves the uploaded file on local machine and returns file's id
    '''

    """
    if request.method == "POST":
        # check if the post request has the file part
        # tbc below code
        if "file" not in request.files:
            error_msg = {
                "error_message":"no file chosen",
                }
            return jsonify(error_msg)
    """

    file = request.files['file']

    # verification if filename is empty
    if file.filename == "":
        error_msg = {
            "error_message":"no file chosen",
            }
        return jsonify(error_msg)

    # verification of file type
    # only pdf- and PDF-files are allowed
    filename = secure_filename(file.filename)
    file_extention = filename[-3::].lower()
    if file_extention == 'pdf': 
        file_id = generate_file_id()
        save_received_pdf(file_id)
        init_db()
        record_id = save_metadata_and_text_to_data_base(file_id)

        # put doc_id in Python dictionary
        doc_id_dictionary = {"id": record_id}
        return jsonify(doc_id_dictionary)

    else:
        error_msg = {
            "error_message":"only .pdf or .PDF-file types are allowed",
            }
        return jsonify(error_msg)



@get_file_info_blueprint.route("/documents/<id>", methods=['GET'])
def processing_meta_link(id):
    '''
    Routing to the endpoint that returns document's metadata in json
    id is id in database
    '''
    
    # checks the highest id in database
    max_id_in_database = session.query(Pdf).count()
    
    # creates an array of existing indexes in database
    list_of_id_in_database = list(range(1, max_id_in_database + 1))
    
    # checks if requested id is a number 
    # and if the index is in database
    if id.isdigit() and int(id) in list_of_id_in_database:    
        pdf_item = session.query(Pdf).filter_by(id=id).first()
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

    else: 
        error_msg = {
            "error_message":"the id you ask does not exist",
            }
        return jsonify(error_msg)
    

@get_text_blueprint.route('/text/<id>.txt', methods=['GET'])
def print_text(id):
    """
    Routing to the endpoint that returns related text from database
    """
    pdf_item = session.query(Pdf).filter_by(id=id).first()
    doc_text_in_dict = {'text': pdf_item.text}
    return jsonify(doc_text_in_dict)