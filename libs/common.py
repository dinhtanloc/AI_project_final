from dotenv import load_dotenv, find_dotenv 
#-----DATA-PREPROCESSING-------
import pandas as pd
from vnstock3 import Vnstock
from bs4 import BeautifulSoup
import psycopg2 
import functools
import json
import numpy as np
import pandas as pd


#------LANGCHAIN---------------
from langchain.llms.openai import OpenAI
from sqlalchemy import create_engine
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
# from langchain_google_vertexai import ChatVertexAI
from langchain_core.runnables import RunnablePassthrough
# from models.lstm_stock_price import model
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
from langchain_community.agent_toolkits import create_sql_agent
# from autogen import RAGAgent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
# from langchain.retrievers import ChromaRetriever
# from langchain.embeddings import ChromaEmbedder
from langchain import LLMChain
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
import getpass
import os
from dotenv import load_dotenv, find_dotenv
from langchain.sql_database import SQLDatabase
from langgraph.prebuilt import ToolNode
from typing import Literal, List
from datetime import datetime, timedelta
from scipy.optimize import minimize
import random as rd
