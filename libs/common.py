#-----DATA-PREPROCESSING-------
import pandas as pd
from vnstock3 import Vnstock
from bs4 import BeautifulSoup


#------LANGCHAIN---------------
from langchain.llms.openai import OpenAI

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain

from dotenv import load_dotenv, find_dotenv # pip install load-dotenv

import psycopg2 # pip install psycopg-binary