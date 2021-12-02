# imports to work with web
from flask import request

# imports to read from pdf
from pdfminer.high_level import extract_text

# imports to extract data from pdf
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

# imports to generate file-id 
import random
import string

# imports to work with databse
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# for verification if upload path exist
import os


# STEPS OF IMPROUVEMENT
# Try to use pprint
# Point to improuve: if file name is the same as existing, get a msg
# check file extention before upload (pdf only)
# delete "debug=True" in main function
# need to add processing state (to be able to share status)
# work with exceptions
# charge out views.py // probably need to move instructions to controller
# tbc if my return is real json
# try to apply jsonify
# add raise exception capture when no db-file and you try to get data
# tbc number of blueprints
# tbc if can keep app in __init__.py outside function


# path to folder where files will be saved
path_to_save_folder = '../uploads/'


# creation and preparation of database
engine = create_engine('sqlite:///pdf.db', echo=False,
                       connect_args={'check_same_thread': False})
connection = engine.connect()
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    Base.metadata.create_all(engine)


class Pdf(Base):
    __tablename__ = 'pdfs'

    id = Column(Integer, primary_key=True)
    author = Column(String)
    creation_date = Column(String)
    modification_date = Column(String)
    creator = Column(String)
    status = Column(String)
    text = Column(String)
    file_id = Column(String)

    def __repr__(self):
        return "<Pdf(author='%s', creation_date='%s', modification_date='%s', creator='%s', status='%s', text='%s', file_id='%s')>" % (
            self.author, self.creation_date, self.modification_date, self.creator, self.status, self.text, self.file_id)



def create_upload_folder_if_needed():
    """
    Upload folder is where pdf files are saved
    If upload folder does not exist, it creates one
    """
    if not os.path.exists(path_to_save_folder): 
        os.makedirs(path_to_save_folder)
     

    
def save_received_pdf(file_id):
    """
    saves uploaded pdf-file to local path 
    uses file_id as a part of file name
    """
    create_upload_folder_if_needed()
    local_file_path = path_to_save_folder + file_id + '.pdf'
    file = request.files['file']
    file.save(local_file_path)


def generate_file_id():
    """ 
    generates id that will be used to save file localy     
    """
    file_id = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    return str(file_id)


def save_metadata_and_text_to_data_base(doc_id):
    """
    saves meta-data and text from pdf to database
    """
    doc_text = extract_text_from_pdf(doc_id)
    meta_data = extract_metadata_from_pdf(doc_id)

    session.add_all([
        Pdf(author=meta_data['author'],
            creation_date=meta_data['creation_date'],
            modification_date=meta_data['modification_date'],
            creator=meta_data['creator'],
            status='ok',
            text=doc_text,
            file_id=doc_id)
    ])

    session.commit()
    pdf_item = session.query(Pdf).filter_by(file_id=doc_id).first()

    return pdf_item.id


def extract_text_from_pdf(doc_id):
    """
    extracts text from pdf-file
    """
    path_to_pdf = path_to_save_folder + doc_id + '.pdf'
    text = extract_text(path_to_pdf)
    return text


def extract_metadata_from_pdf(doc_id):
    """
    extracts metadata from pdf-file
    and returns dictionary with metadata inside
    """
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
