import functools
from vnstock3 import Vnstock
import json
import numpy as np
import pandas as pd
from langchain_core.runnables import RunnablePassthrough

from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
from langchain_community.agent_toolkits import create_sql_agent
from autogen import RAGAgent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.retrievers import ChromaRetriever
from langchain.embeddings import ChromaEmbedder
from langchain import LLMChain
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
import getpass
import os
from langchain.sql_database import SQLDatabase
from langgraph.prebuilt import ToolNode, StateGraph, AgentState
from typing import Literal


os.environ["OPENAI_API_KEY"] = getpass.getpass("Please provide your OPENAI_API_KEY:")
os.environ["POSTGRESQL_DBMS_KEY"] = getpass.getpass("Please provide your POSTGRESQL_DBMS_KEY:")

db = SQLDatabase.from_uri(os.getenv('POSTGRESQL_DBMS_KEY'))


###EUT
@tool
def calculate_utility(outcome: float, risk_aversion: float) -> float:
    """Calculate utility based on the outcome and risk aversion coefficient."""
    return outcome ** (1 - risk_aversion) / (1 - risk_aversion)
@tool
def calculate_expected_utility(probabilities: np.ndarray, utilities: np.ndarray) -> float:
    """Calculate the expected utility."""
    if len(probabilities) != len(utilities):
        raise ValueError("Probabilities and utilities must have the same length.")
    
    expected_utility = np.dot(probabilities, utilities)
    return expected_utility

###MVP
@tool
def calculate_portfolio_return(returns: np.ndarray, weights: np.ndarray) -> float:
    """Calculate the annualized portfolio return."""
    return np.dot(returns.mean(), weights) * 252

@tool
def calculate_portfolio_volatility(returns: np.ndarray, weights: np.ndarray) -> float:
    """Calculate the annualized portfolio volatility."""
    return np.dot(weights, np.dot(returns.cov() * 252, weights)) ** 0.5  # Annualized volatility

@tool
def calculate_sharpe_ratio(returns: np.ndarray, weights: np.ndarray, risk_free_rate: float) -> float:
    """Calculate the Sharpe ratio of the portfolio."""
    port_return = calculate_portfolio_return(returns, weights)
    port_volatility = calculate_portfolio_volatility(returns, weights)
    sharpe_ratio = (port_return - risk_free_rate) / port_volatility
    return sharpe_ratio


### CAPM
@tool
def calculate_beta(asset_returns: np.ndarray, market_returns: np.ndarray) -> float:
    """Calculate the beta of an asset."""
    covariance_matrix = np.cov(asset_returns, market_returns)
    beta = covariance_matrix[0, 1] / covariance_matrix[1, 1]
    return beta

@tool
def calculate_capm(risk_free_rate: float, beta: float, market_return: float) -> float:
    """Calculate the expected return of an asset using the CAPM formula."""
    expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
    return expected_return

####Get API
@tool
def generate_prompt_with_date(prompt):
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")
    full_prompt = f"{prompt} Today's date is {current_date}."
    return full_prompt

@tool
def get_company_information(symbol):
    """Get company information such as overview, profile, shareholders, subsidiaries, and officers."""
    company = Vnstock().stock(symbol=symbol, source='TCBS').company
    
    try:
        overview = company.overview()
        profile = company.profile()  # Assuming profile is another method; adjust if incorrect
        shareholders = company.shareholders()
        subsidiaries = company.subsidiaries()
        officers = company.officers()
        
        result = {
            "overview": overview,
            "profile": profile,
            "shareholders": shareholders,
            "subsidiaries": subsidiaries,
            "officers": officers
        }
    except Exception as e:
        result = {"error": str(e)}
    
    return json.dumps(result)


@tool
def get_api_stock(symbols, startday, endday):
    """Get stock data for a given symbol and date range."""
    stock = Vnstock().stock(symbol=symbols, source='TCBS')
    
    try:
        df = stock.quote.history(start=startday, end=endday, interval='1m')
        
        if not df.empty:
            df = df.map(lambda x: x.isoformat() if isinstance(x, (pd.Timestamp, pd.Timestamp)) else x)
            result = df.to_dict(orient='records')
        else:
            result = {"error": "No data found for the given range"}
    
    except Exception as e:
        result = {"error": str(e)}
    
    return json.dumps(result)


@tool
def get_api_income_statement(symbols):
    stock = Vnstock().stock(symbol=symbols, source='TCBS')
    try:
        df = stock.finance.income_statement(period='year', lang='en')
        if not df.empty:
            result = df.to_dict(orient='records')
        else:
            result = {"error": "No data found for the given range"}
    except Exception as e:
        result = {"error": str(e)}
    
    return json.dumps(result)

@tool
def get_api_balance_sheet(symbols):
    stock = Vnstock().stock(symbol=symbols, source='TCBS')
    try:
        df = stock.finance.balance_sheet(period='year', lang='en')
        if not df.empty:
            result = df.to_dict(orient='records')
        else:
            result = {"error": "No data found for the given range"}
    except Exception as e:
        result = {"error": str(e)}
    
    return json.dumps(result)


tools = [
    calculate_utility,
    calculate_expected_utility,
    calculate_portfolio_return,
    calculate_portfolio_volatility,
    calculate_sharpe_ratio,
    calculate_beta,
    calculate_capm,
    generate_prompt_with_date,
    get_company_information,
    get_api_stock,
    get_api_income_statement,
    get_api_balance_sheet,
]

examples = [
    [
        HumanMessage("Hiện nay, một danh mục đầu tư của tôi bao gồm các mã cổ phiếu của sàn VNINDEX như là AAM, XPH, YEG, AAT. Tôi nên tối ưu hóa danh mục đầu tư như thế nào? ", name="example_user"),
        AIMessage("", name="example_assistant", tool_calls=[{"name": "multiply", "args": {"x": 317253, "y": 128472}, "id": "1"}]),
        ToolMessage("16505054784", tool_call_id="1"),
        AIMessage("", name="example_assistant", tool_calls=[{"name": "add", "args": {"x": 16505054784, "y": 4}, "id": "2"}]),
        ToolMessage("16505054788", tool_call_id="2"),
        AIMessage("The product of 317253 and 128472 plus four is 16505054788", name="example_assistant"),
    ],
    [
        HumanMessage("Theo bạn hiện nay, tình hình công ty mã A32 có chuyển biến như thế nào, liệu có nên đầu tư cho vào nó không"),
        AIMessage("", name="example_assistant", tool_calls=[{"name": "multiply", "args": {"x": 3, "y": 2}, "id": "1"}]),
        ToolMessage("6", tool_call_id="1"),
        AIMessage("", name="example_assistant", tool_calls=[{"name": "add", "args": {"x": 5, "y": 6}, "id": "2"}]),
        ToolMessage("11", tool_call_id="2"),
        AIMessage("5 plus 3 times 2 is 11", name="example_assistant"),
    ],
    [
        HumanMessage("Bạn hãy điều tra và tóm tắt về tiểu sử công ty mã A32 cùng với tình hình kinh doanh công ty trong suốt sáu tháng qua"),
        AIMessage("", name="example_assistant", tool_calls=[{"name": "multiply", "args": {"x": 3, "y": 2}, "id": "1"}]),
        ToolMessage("6", tool_call_id="1"),
        AIMessage("", name="example_assistant", tool_calls=[{"name": "add", "args": {"x": 5, "y": 6}, "id": "2"}]),
        ToolMessage("11", tool_call_id="2"),
        AIMessage("5 plus 3 times 2 is 11", name="example_assistant"),
    ],
    [
        HumanMessage("Đánh giá công ty này có hoạt động ổn định hay không trong suốt 6 tháng quá, check lại sự kiện kèm tin tức để đánh giá mức độ của công ty"),
        AIMessage("", name="example_assistant", tool_calls=[{"name": "multiply", "args": {"x": 3, "y": 2}, "id": "1"}]),
        ToolMessage("6", tool_call_id="1"),
        AIMessage("", name="example_assistant", tool_calls=[{"name": "add", "args": {"x": 5, "y": 6}, "id": "2"}]),
        ToolMessage("11", tool_call_id="2"),
        AIMessage("5 plus 3 times 2 is 11", name="example_assistant"),
    ],
]


llm = ChatOpenAI(model="gpt-4-1106-preview")
llm_with_tools = llm.bind_tools(tools)

system="""Bạn là một chuyên gia chơi chứng khoán trong lĩnh vực kinh tế đầu tư tại thị trường chứng khoán Việt Nam. Sử dụng các tool được cung cấp như một ví dụ để đưa ra những lời khuyên hữu ích để người chơi mới tại Việt Nam lựa chọn và tối ưu hóa danh mục đầu tư, đầu tư chứng khoán thành công
"""

few_shot_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        *examples,
        ("human", "{query}"),
    ]
)

chain = {"query": RunnablePassthrough()} | few_shot_prompt | llm_with_tools
chain.invoke("Whats 119 times 8 minus 20").tool_calls
