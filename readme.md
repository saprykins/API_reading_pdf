# API TO GET INFORMATION FROM PDF

# OVERVIEW
API that receives and saves pdf file, extracts and saves its text and meta-data in local database.  
API allows to retrieve text and meta-data of a pdf-file previously uploaded via its id.  
No authentication required

# USAGE
POST	/documents				upload a new pdf, responds a document ID
GET		/documents/<id> 		describe document processing state (pending, success, failure), metadata and links to contents 
GET		/text/<id>.txt 		a way to read the extracted text

# INSTALLATION (UBUNTU OS)

The application requires Python installed.  

 * For more details about Python installation, check the following link:  
 https://www.python.org/downloads/  

Download the latest version of applicaton from the link below:  
https://github.com/saprykins/API_reading_pdf/archive/refs/heads/master.zip  

Create a new folder for the application  

Unzip the downloaded zip file in the folder you have just created  

Create vitual environment  

* You can create it from command line:  
  ```
  $ sudo virtualenv <my_env_name>
  ```
  where <my_env_name> is the name of the virtual environment you would like to create.  

  As an example, you can call it venv and simply type: 
  ```
  $ sudo virtualenv venv
  ```
* If you do not have virtual environment tool installed, you can install it from command line:    
  ```
  $ sudo apt install python3-virtualenv
  ```

Activate the virtual environment you have just created: 
```
$ source <my_env_name>/bin/activate
```
* In case you created virtual environment "venv" you activate it as:  
  ```
  $ source ./venv/bin/activate
  ```

* For more details about virtual environment, check the following link:  
  https://docs.python.org/3/tutorial/venv.html  

Install the packages that application requires typing in command line:  
```
$ pip install -r requirements.txt
```

# TUTORIAL

## Run the app  

To run the application after installation, type the following in command line:  
```
$ python ./flaskr/__init__.py
```
The application runs while the the command line window is open.  

* You can check in your web-browser that the application works by typing in address line of your browser:  

  http://localhost:5000/  

  You should see text "Index page" in your browser

## Upload a pdf-file  

Open a new terminal window, to let your application run in previous terminal window  

To upload a pdf-file "sample.pdf" using command line, you can use curl-command  

* In case curl tool is not installed you can do this in command line:  
  ```
  $ sudo apt  install curl   
  ```

In terminal go to the folder where the file you want to send is located and type:  
```
$  curl -sF file=@"sample.pdf" http://localhost:5000/documents
```
* Standard response returns a json file in the following format:  
  ```
  {
      "id": 1
  }
  ```
  where 1 is id number of the record in database.  

* At this moment the pdf-file is saved on your local machine, text and metadata are saved in local sqlite database.  

* You can use this id to retrieve the information about the file.  

## Get metadata  

To retrive metadata about a file, you need its id (or document_id) that you get on previous step.  
```
curl -s http://localhost:5000/documents/<document_id>
```
* where document_id should be replaced by a number.  

* In case you sent at least one file, you can retrieve metadata related to the record 1 in database by typing:  
  ```
  curl -s http://localhost:5000/documents/1
  ```
  
The standard response returns json-file in format:
```
{
  "author": "GPL Ghostscript SVN PRE-RELEASE 8.62",
  "creation_date": "D:20080201104827-05'00'",
  "creator": "dvips(k) 5.86 Copyright 1999 Radical Eye Software",
  "file_id": "tpvtajdvrlrqdecv",
  "link_to_content": "http://localhost:5000/text/1.txt",
  "modification_date": "D:20080201104827-05'00'",
  "status": "success"
}
```

Instead of curl, you can also retrieve metadata via web-browser  

Type in address line http://localhost:5000/documents/<document_id> 

* where document_id should be replaced by a number.  

* In case you sent at least one file, you can retrieve metadata related to the record 1 in database by typing:  

  http://localhost:5000/documents/1  

## Get text  

To retrive text from database, you need document_id. Type the following in command line to retrieve it:  
```
$ curl -s http://localhost:5000/text/<document_id>.txt
```
* where document_id should be replaced by a number.  

* In case you sent at least one file, you can retrieve metadata related to the record 1 in database by typing:  
  ```
  $ curl -s http://localhost:5000/text/1.txt
  ```
* Keep in mind ".txt" after document_id

Standard response returns json-file in format:  
```
{
    "text": "text from pdf"
}
```

Instead of curl, you can also retrieve text via web-browser  

Type in address line http://localhost:5000/text/<document_id>.txt 

* where document_id should be replaced by a number.  

* In case you sent at least one file, you can retrieve metadata related to the record 1 in database by typing:  

  http://localhost:5000/text/1.txt  

## Stop the application

To stop the application, type "ctr + C" in terminal window where it was launched or close the terminal window.  


## Test the application
To launch tests, go to the project's top-level directory (API_reading_pdf)  
and launch the command  
```
$ export PYTHONPATH="venv/lib/python3.9/site-packages/"
$ coverage run -m pytest
$ coverage report
```
For more details, you can check what are the line numbers that were not covered in tests
```
$ coverage report -m
```
To create a detailed html report in "API_reading_pdf/htmlcov/index.html", type the following
```
$ coverage html
```

## Check code quality with Pylint
To check if the style of code in files is pythonic you can use Pylint.  
To do that go to flaskr directory and type
```
$ pylint ./flaskr
```
You can also check each file using  
```
$ pylint model.py
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

<!---
if not ubuntu
do i need python
-->

test-project/
├── data        
├── deliver           # Final analysis, code, & presentations
├── develop           # Notebooks for exploratory analysis
├── src               # Scripts & local project modules
├── venv              # Scripts & local project modules
└── tests

The application allows user to upload pdf-file, to extract text and metadata from it and displays it to user. 
It is based on three endpoints
