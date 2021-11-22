# working with web
from flask import request

# reading from pdf
from pdfminer.high_level import extract_text

# extracting data from pdf
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

# file-id generator
import random
import string

# working with databse
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# STEPS OF IMPROUVEMENT
# Try to use pprint
# Point to improuve: if file name is the same as existing, get a msg
# check file extention before upload (pdf only)
# delete "debug=True" in main function
# need to add processing state (to be able to share status)
# for docs, you can include advice to use gitk ou git log --graph to show commits
# generate upload-folder automatically if it doens't exist
# work with exceptions
# charge out views.py // probably need to move instructions to controller
# tbc if my return is real json
# try to apply jsonify
# add raise exception capture when no db-file and you try to get data
# tbc number of blueprints
# tbc if can keep app in __init__.py outside function

# global attributes
path_to_save_folder = '../uploads/'

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


def save_received_pdf(file_id):
    # save pdf-file
    local_file_path = path_to_save_folder + file_id + '.pdf'
    file = request.files['file']
    file.save(local_file_path)


def generate_file_id():
    file_id = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    return str(file_id)


# saves meta-data and text from pdf to database
def save_metadata_and_text_to_data_base(doc_id):
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
