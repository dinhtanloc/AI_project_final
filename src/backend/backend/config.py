
import os
import yaml
from dotenv import load_dotenv, find_dotenv
from pyprojroot import here
from sentence_transformers import SentenceTransformer

load_dotenv(find_dotenv())

with open(here("config/project_config.yml")) as cfg:
    app_config = yaml.load(cfg, Loader=yaml.FullLoader)


class LoadProjectConfig:
    def __init__(self) -> None:
        os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
        os.environ["LANGCHAIN_TRACING_V2"] = app_config["langsmith"]["tracing"]
        os.environ["LANGCHAIN_PROJECT"] = app_config["langsmith"]["project_name"]
        self.memory_dir = here(app_config["memory"]["directory"])
        self.embedding_model = SentenceTransformer("keepitreal/vietnamese-sbert")


        #keys project
        self.djangoprj = os.getenv('DJANGO_keys')
        # database settings
        self.dbname=os.getenv('DB_name')
        self.dbuser=os.getenv('DB_user')
        self.dbpassword=os.getenv('DB_password')
        self.dbport=os.getenv('DB_port')
        #chatbot database settings
        self.postgrest_dbms = os.getenv('POSTGRESQL_DBMS_KEY')
        self.mongodb_uri = os.getenv('MONGODB_URL')

        self.openai =os.getenv("OPEN_API_KEY")
        self.tavily = os.getenv("TAVILY_API_KEY")

        #adminData
        self.admindata_docdir= app_config["admindata"]["doc_dir"]
        self.admindata_chunksize= app_config["admindata"]["chunk_size"]
        self.admindata_chunk_overlap= app_config["admindata"]["chunk_overlap"]
        self.admindata_dbname= app_config["admindata"]["db_name"]
        self.admindata_collection=app_config["admindata"]["collection_name"]
        self.admindata_mongodb_uri = os.getenv('MONGODB_URL')

