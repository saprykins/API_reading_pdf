# API_TO_GET_PDF_INFORMATION

# OVERVIEW
API that uploads and saves pdf file, extracts and saves its text and meta-data in local database.  
API allows to get text and meta-data about the pdf-file previously uploaded via its id/reference.  
No authentication required

# INSTALLATION
<!---
? you need Python installed
-->

Create new folder  

Go to the new folder  

Download the applicaton to local machine from the link below  
https://github.com/saprykins/API_reading_pdf/archive/refs/heads/master.zip  

Unzip the folder  

Create virtual environment in the following way:  
```
$ virtualenv <my_env_name>
```
where <my_env_name> is the name of your new environment. No need to use angle brackets. So you can simply type: 
```
$ virtualenv venv
```

Activate the environment you have just created: 
```
$ source <my_env_name>/bin/activate
```
Install the packages that application needs
```
$ pip install -r requirements.txt
```

# TUTORIAL
To launch the application after installation type in command line:  
```
$ python __init__.py
```
The application works while the the command line window is open.  

You can check in your web-browser that the application works by typing in address line:  
http://localhost:5000/  

## Upload a pdf-file  

To upload a pdf-file "sample.pdf" using command line, go to the folder where it is located and type: 
```
$  curl -sF file=@"sample.pdf" http://localhost:5000/documents
```
Standard response returns json file in format:  
```
{
    "id": 1
}
```
where 1 is id / reference number of the record in database.  

At this moment the pdf-file is saved on local machine, text and metadata are saved in database.  

You can use this id to retrieve the information about the file.  

## Get metadata  

To retrive information about a file, you need document_id that you get in previous step. 
```
curl -s http://localhost:5000/documents/document_id
```
Where document_id should be replaced by the id / reference.  
The standard response returns json-file in format
```
{
  "author": "GPL Ghostscript SVN PRE-RELEASE 8.62",
  "creation_date": "D:20080201104827-05'00'",
  "creator": "dvips(k) 5.86 Copyright 1999 Radical Eye Software",
  "file_id": "tpvtajdvrlrqdecv",
  "link_to_content": "http://localhost:5000/text/2.txt",
  "modification_date": "D:20080201104827-05'00'",
  "status": "success"
}
```

## Get text  

To retrive text from a file, you need document_id. Type the following command to retrieve it:  
```
$ curl -s http://localhost:5000/text/document_id.txt
```
where document_id should be replaced by a number.  

Standard response returns json-file in format:  
```
{
    "text": "text from pdf"
}
```

<!---
step-by-step instructions for using APIs to accomplish specific tasks or workflows with detailed explanations about using the endpoints and parameters in each function call or method invocation.

can get pdf or PDF files

when no you send not pdf
{
# "status":500,
"error_message":"the file-type you send is not pdf",
}

for docs, you can include advice to use gitk ou git log --graph to show commits

# REFERENCE
structure, parameters, and return values for each function or method in an API.

it creates a folder if it doesn't exist
-->