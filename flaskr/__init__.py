import json
from model import generate_file_id, save_metadata_and_text_from_pdf_to_text_files, save_received_pdf, extract_metadata_from_pdf, get_doc_text_in_dictionary
from flask import Flask


# initialization of WSGI application
app = Flask(__name__)


# routing to index page
@app.route("/")
def index():
    return str("Index page")


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

    save_received_pdf(file_id)
    save_metadata_and_text_from_pdf_to_text_files(file_id)

    # doc_id in Python dictionary
    doc_id_dictionary = {"id": file_id, }

    # convert into JSON:
    doc_id_in_json = json.dumps(doc_id_dictionary)
    return doc_id_in_json


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

    # return file_path_link
    file_path_link = 'http://localhost:5000/text/' + file_id + '_text.txt'
    meta_link = 'http://localhost:5000/text/' + file_id + '_meta.txt'

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
    file_id = id

    # convert into JSON:
    doc_text_in_json = json.dumps(get_doc_text_in_dictionary(file_id))
    return doc_text_in_json


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
