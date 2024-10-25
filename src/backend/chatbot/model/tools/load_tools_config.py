import os
import yaml
from dotenv import load_dotenv
from pyprojroot import here

load_dotenv()


class LoadToolsConfig:

    def __init__(self) -> None:
        with open(here("config/tools_config.yml")) as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)

        # Set environment variables
        os.environ['OPENAI_API_KEY'] = os.getenv("OPEN_API_KEY")
        os.environ['TAVILY_API_KEY'] = os.getenv("TAVILY_API_KEY")
        self.stock_db = os.getenv("POSTGRESQL_DBMS_KEY")


        # Primary agent
        self.primary_agent_llm = app_config["primary_agent"]["llm"]
        self.primary_agent_llm_temperature = app_config["primary_agent"]["llm_temperature"]

        # Internet Search config
        self.tavily_search_max_results = int(
            app_config["tavily_search_api"]["tavily_search_max_results"])

        # Document RAG configs
        self.policy_rag_llm_temperature = float(
            app_config["document_rag_pdf"]["llm_temperature"])
        self.policy_rag_embedding_model = app_config["document_rag_pdf"]["embedding_model"]
        # self.policy_rag_vectordb_directory = str(here(
        #     app_config["document_rag_pdf"]["vectordb"]))  # needs to be strin for summation in chromadb backend: self._settings.require("persist_directory") + "/chroma.sqlite3"
        self.policy_rag_k = app_config["document_rag_pdf"]["k"]
        self.policy_rag_collection_name = app_config["document_rag_pdf"]["collection_name"]

        # History RAG configs
        self.history_rag_llm_temperature = float(
            app_config["chatbot_history"]["llm_temperature"])
        self.history_rag_embedding_model = app_config["chatbot_history"]["embedding_model"]
        # self.history_rag_vectordb_directory = str(here(
        #     app_config["chatbot_history"]["vectordb"]))  # needs to be strin for summation in chromadb backend: self._settings.require("persist_directory") + "/chroma.sqlite3"
        self.history_rag_k = app_config["chatbot_history"]["k"]
        self.history_rag_collection_name = app_config["chatbot_history"]["collection_name"]
        self.history_rag_db_name = app_config["chatbot_history"]["db_name"]


        #SQL Agent configs
        self.sqldb_directory = str(here(
            app_config["sqlagent_configs"]["sqldb_dir"]))
        self.sqlagent_llm = app_config["sqlagent_configs"]["llm"]
        self.sqlagent_llm_temperature = float(
            app_config["sqlagent_configs"]["llm_temperature"])


        # Graph configs
        self.thread_id = str(
            app_config["graph_configs"]["thread_id"])