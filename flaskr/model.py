# working with web

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


# global attributes
path_to_save_folder = './uploads/'


def save_received_pdf(file_id):
    # save pdf-file
    local_file_path = path_to_save_folder + file_id + '.pdf'
    file = request.files['file']
    file.save(local_file_path)


def get_doc_text_in_dictionary(file_id):
    file_path = path_to_save_folder + file_id + '_text.txt'

    with open(file_path) as feed:
        text = feed.read()

        # doc_id in Python dictionary
        doc_text_in_dictionary = {"text": text, }

        return doc_text_in_dictionary


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
