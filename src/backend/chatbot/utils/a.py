import os
import yaml
from pyprojroot import here
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv, find_dotenv
import pymongo
load_dotenv(find_dotenv())
os.environ['OPENAI_API_KEY'] = os.getenv("OPEN_API_KEY")

with open(here("config/tools_config.yml")) as cfg:
    app_config = yaml.load(cfg, Loader=yaml.FullLoader)

CHUNK_SIZE = app_config["document_rag_pdf"]["chunk_size"]
CHUNK_OVERLAP = app_config["document_rag_pdf"]["chunk_overlap"]
EMBEDDING_MODEL = app_config["document_rag_pdf"]["embedding_model"]
MONGODB_URI = os.getenv('MONGODB_URL') 
COLLECTION_NAME = app_config["document_rag_pdf"]["collection_name"]
DB_NAME = app_config["document_rag_pdf"]["db_name"]  
DOC_DIR = app_config["document_rag_pdf"]["unstructured_docs"]



# prepare_db_instance.run()
from pathlib import Path
print(MONGODB_URI)
client = pymongo.MongoClient(MONGODB_URI)
db = client['dinhtanloc']
collection = db['rag_test']
print(client['dinhtanloc']['rag_test'].count_documents({}))
project_root = Path(__file__).resolve().parent.parent
print(project_root)
print(here(DOC_DIR))
# print("Number of vectors in MongoDB collection:", prepare_db_instance.collection.count_documents({}), "\n\n")