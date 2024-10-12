
import os
import yaml
from dotenv import load_dotenv, find_dotenv
from pyprojroot import here

load_dotenv(find_dotenv())

with open(here("config/project_config.yml")) as cfg:
    app_config = yaml.load(cfg, Loader=yaml.FullLoader)


class LoadProjectConfig:
    def __init__(self) -> None:
        os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
        os.environ["LANGCHAIN_TRACING_V2"] = app_config["langsmith"]["tracing"]
        os.environ["LANGCHAIN_PROJECT"] = app_config["langsmith"]["project_name"]
        self.memory_dir = here(app_config["memory"]["directory"])
