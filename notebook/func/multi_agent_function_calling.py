from langchain_openai import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain import LLMChain
from langchain.retrievers import ChromaRetriever
from langchain.embeddings import ChromaEmbedder
from langchain_community.agent_toolkits import create_rag_agent
import autogen
import os
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
config_list = [
    {
        "model": "gpt-4",
        "api_key": os.getenv("OPENAI_API_KEY"),
    }
]

def perform_arithmetic_operations(a: int, b: int) -> dict:
    """
    Perform basic arithmetic operations on two integers.
    
    Parameters:
    - a (int): First integer.
    - b (int): Second integer.
    
    Returns:
    - dict: A dictionary containing the results of arithmetic operations.
    """
    return {
        "sum": a + b,
        "difference": a - b,
        "product": a * b,
        "quotient": a / b if b != 0 else "Division by zero error"
    }



def generate_sql_query(description: str) -> str:
    """
    Generate an SQL query from a natural language description using LangChain.
    
    Parameters:
    - description (str): The natural language description of the query.
    - db_uri (str): Database URI to connect to the SQL database.
    
    Returns:
    - str: Generated SQL query.
    """
    # Initialize the OpenAI LLM and SQLDatabase
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    db = SQLDatabase.from_uri(os.getenv('POSTGRESQL_DBMS_KEY'))
    
    # Create the SQL agent
    agent = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
    
    # Generate the SQL query
    sql_query = agent(description)
    return sql_query

def rag_query(question: str, collection_name: str, embedding_function) -> str:
    """
    Answer a question using RAG (Retrieval-Augmented Generation) with LangChain.
    
    Parameters:
    - question (str): The question to be answered.
    - collection_name (str): The name of the Chroma collection.
    - embedding_function: Function to generate embeddings.
    - db_uri (str): Database URI to connect to the SQL database.
    
    Returns:
    - str: The answer to the question.
    """
    # Initialize the Chroma retriever
    retriever = ChromaRetriever(
        collection_name=collection_name,
        embedding_function=embedding_function,
    )
    
    # Initialize the LLM chain
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    llm_chain = LLMChain(
        prompt_template="Provide a detailed answer to the following question: {question}",
        llm=llm
    )
    
    # Initialize the RAG agent
    rag_agent = create_rag_agent(
        retriever=retriever,
        reader=llm_chain,
        embedder=ChromaEmbedder()  # Ensure to use an appropriate embedder
    )
    
    # Get the answer from the RAG agent
    answer = rag_agent.run(question)
    return answer


llm_config = {
    "functions": [
        {
            "name": "perform_arithmetic_operations",
            "description": "Perform basic arithmetic operations on two integers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "First integer.",
                    },
                    "b": {
                        "type": "integer",
                        "description": "Second integer.",
                    },
                },
                "required": ["a", "b"],
            },
        },
        {
            "name": "generate_sql_query",
            "description": "Generate an SQL query from a natural language description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Natural language description of the SQL query.",
                    },
                    
                },
                "required": ["description"],
            },
        },
        {
            "name": "rag_query",
            "description": "Answer a question using Retrieval-Augmented Generation (RAG) with LangChain.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question to be answered.",
                    },
                    "collection_name": {
                        "type": "string",
                        "description": "The name of the Chroma collection.",
                    },
                    "embedding_function": {
                        "type": "string",
                        "description": "Function to generate embeddings.",
                    },
                  
                },
                "required": ["question", "collection_name", "embedding_function"],
            },
        }
    ],
    "config_list": config_list,
    "timeout": 120,
}




# Khởi tạo các agents
chatbot = autogen.AssistantAgent(
    name="chatbot",
    system_message="For coding tasks, only use the functions you have been provided with. Reply TERMINATE when the task is done.",
    llm_config=llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "coding_2",
        "use_docker": False,
    },
)

user_proxy.register_function(
    function_map={
        "perform_arithmetic_operations": perform_arithmetic_operations,
        "generate_sql_query": generate_sql_query,
        "rag_query": rag_query,
    }
)
