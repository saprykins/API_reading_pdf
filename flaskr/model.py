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
    """
    Represents pdf-file
    It is used to save metadata, text of pdf-file 
    and to retrive this information
    """

    # Table name in the database
    __tablename__ = 'pdfs'
    # identifier in database
    id = Column(Integer, primary_key=True)
    # author of pdf-file
    author = Column(String)
    # date of creation of pdf-file
    creation_date = Column(String)
    # last modification of pdf-file
    modification_date = Column(String)
    # creator of pdf-file
    creator = Column(String)
    # status of pdf-file
    status = Column(String)
    # text inside pdf-file
    text = Column(String)
    # name of pdf file that was saved locally
    file_id = Column(String)

    def __repr__(self):
        return "<Pdf(author='%s', creation_date='%s', modification_date='%s', creator='%s', status='%s', text='%s', file_id='%s')>" % (
            self.author, self.creation_date, self.modification_date, self.creator, self.status, self.text, self.file_id)


def id_in_database(id): 
    """
    verifies if id is in dabase and if it is digit
    """
    
    # default verification result is False
    result = False

    # checks the highest id in database
    max_id_in_database = session.query(Pdf).count()
    
    # creates an array of existing indexes in database
    list_of_id_in_database = list(range(1, max_id_in_database + 1))
    
    # checks if requested identifier is a number 
    # and if the id is in database
    if id.isdigit() and int(id) in list_of_id_in_database: 
        result = True
    return result


def create_upload_folder_if_needed():
    """
    Upload folder is where pdf files are saved
    If upload folder does not exist, it creates one
    """
    if not os.path.exists(path_to_save_folder): 
        os.makedirs(path_to_save_folder)
     

    
def save_received_pdf(file_id):
    """
    Saves uploaded pdf-file to local path 
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

    # extracts text and metadata from pdf
    doc_text = extract_text_from_pdf(doc_id)
    meta_data = extract_metadata_from_pdf(doc_id)

    # saves information in database
    session.add_all([
        Pdf(author=meta_data['author'],
            creation_date=meta_data['creation_date'],
            modification_date=meta_data['modification_date'],
            creator=meta_data['creator'],
            # status is success since the file is saved locally
            status='success',
            text=doc_text,
            file_id=doc_id)
    ])
    session.commit()
    
    # gets the record from database using pdf-file name
    pdf_item = session.query(Pdf).filter_by(file_id=doc_id).first()
    
    # returns identifier of the record in database 
    return pdf_item.id


def extract_text_from_pdf(doc_id):
    """
    extracts text from pdf-file
    """
    # gets previously saved pdf file locally
    path_to_pdf = path_to_save_folder + doc_id + '.pdf'
    
    # extracts text from the pdf
    text = extract_text(path_to_pdf)
    return text


def extract_metadata_from_pdf(doc_id):
    """
    extracts metadata from pdf-file
    and returns dictionary with metadata inside
    """
    # gets previously saved pdf file locally
    path_to_pdf = path_to_save_folder + doc_id + '.pdf'
    
    # extracts metadata from the pdf
    with open(path_to_pdf, 'rb') as file:
        parser = PDFParser(file)
        doc = PDFDocument(parser)

        # creates temporary dictionary to save metadata
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
