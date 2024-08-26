import functools
from vnstock3 import Vnstock
import json
import numpy as np
import pandas as pd
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
load_dotenv(find_dotenv())



os.environ["OPENAI_API_KEY"] = getpass.getpass("Please provide your OPENAI_API_KEY:")
os.environ["POSTGRESQL_DBMS_KEY"] = getpass.getpass("Please provide your POSTGRESQL_DBMS_KEY:")

db = SQLDatabase.from_uri(os.getenv('POSTGRESQL_DBMS_KEY'))


###EUT
@tool
def calculate_utility(outcome: float, risk_aversion: float) -> float:
    """Calculate utility based on the outcome and risk aversion coefficient."""
    return outcome ** (1 - risk_aversion) / (1 - risk_aversion)
@tool
def calculate_expected_utility(probabilities: List[float], utilities: List[float]) -> float:
    """Calculate the expected utility."""
    if len(probabilities) != len(utilities):
        raise ValueError("Probabilities and utilities must have the same length.")
    
    expected_utility = np.dot(probabilities, utilities)
    return expected_utility


@tool
def porfolio_optimize_EUT():
    pass

###MVP
@tool
def calculate_portfolio_return(returns: List[float], weights: List[float]) -> float:
    """Calculate the annualized portfolio return."""
    return np.dot(returns.mean(), weights) * 252

@tool
def calculate_portfolio_volatility(returns: List[float], weights: List[float]) -> float:
    """Calculate the annualized portfolio volatility."""
    return np.dot(weights, np.dot(returns.cov() * 252, weights)) ** 0.5  # Annualized volatility

@tool
def calculate_sharpe_ratio(returns: List[float], weights: List[float], risk_free_rate: float) -> float:
    """Calculate the Sharpe ratio of the portfolio."""
    port_return = calculate_portfolio_return(returns, weights)
    port_volatility = calculate_portfolio_volatility(returns, weights)
    sharpe_ratio = (port_return - risk_free_rate) / port_volatility
    return sharpe_ratio

@tool
def portfolio_optimize(returns, sharpe_ratio_or_variance=True):
    """
    Tối ưu hóa danh mục đầu tư dựa trên tỷ lệ Sharpe hoặc biến động.
    
    Parameters:
    - returns (pd.DataFrame): DataFrame chứa lợi suất của các cổ phiếu.
    - sharpe_ratio_or_variance (bool): Nếu True, tối ưu hóa theo tỷ lệ Sharpe; nếu False, tối ưu hóa theo biến động.
    
    Returns:
    - optimal_weights (dict): Tỷ trọng tối ưu của các cổ phiếu trong danh mục đầu tư dưới dạng từ điển.
    """
    returns = json.loads(returns)
    returns = pd.DataFrame([returns])
    # returns=returns[returns.columns[1:]]
    # print(returns)
    num_assets = len(returns.columns)
    # print('haha',num_assets)
    init_guess = num_assets * [1. / num_assets]
    bounds = tuple((0, 1) for asset in range(num_assets))
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    
    if sharpe_ratio_or_variance:
        result = minimize(lambda x: -calculate_sharpe_ratio(x, returns), init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    else:
        result = minimize(lambda x: calculate_portfolio_volatility(x, returns), init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    
    # Chuyển đổi tỷ trọng tối ưu thành từ điển với tên cổ phiếu
    optimal_weights = dict(zip(returns.columns, result.x))
    
    return optimal_weights

### CAPM
@tool
def calculate_beta(asset_returns: List[float], market_returns: List[float]) -> float:
    """Calculate the beta of an asset."""
    covariance_matrix = np.cov(asset_returns, market_returns)
    beta = covariance_matrix[0, 1] / covariance_matrix[1, 1]
    return beta

@tool
def calculate_capm(risk_free_rate: float, beta: float, market_return: float) -> float:
    """Calculate the expected return of an asset using the CAPM formula."""
    expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
    return expected_return


#### Make prediction
@tool
def predict_future_prices(symbols, n):
    """
    Dự đoán giá cổ phiếu trong tương lai dựa trên dữ liệu đầu vào.
    
    Parameters:
    - data (list of dict): Danh sách các từ điển chứa dữ liệu với cột 'idx_time', 'AAA', và 'A32'.
    - n (int): Số tháng từ ngày hiện tại để dự đoán.
    
    Returns:
    - future_df (pd.DataFrame): DataFrame chứa dự đoán giá cổ phiếu trong tương lai.
    """
    data=get_api_portfolio(symbols)

    try:
        df = pd.DataFrame(eval(data))
    except ValueError as e:
        print(f"Error creating DataFrame: {e}")
        return
    
    if df.empty or not {'idx_time', 'AAA', 'A32'}.issubset(df.columns):
        print("Data không hợp lệ. Đảm bảo dữ liệu chứa các cột 'idx_time', 'AAA', và 'A32'.")
        return
    
    df['idx_time'] = pd.to_datetime(df['idx_time'] + '-01', format='%Y-%m-%d')
    
    df['days'] = (df['idx_time'] - df['idx_time'].min()).dt.days
    
    df = df.dropna(subset=['AAA', 'A32'])
    
    degree = 2
    
    coeffs_AAA = np.polyfit(df['days'], df['AAA'], degree)
    coeffs_A32 = np.polyfit(df['days'], df['A32'], degree)
    
    # Tạo dãy tháng trong tương lai
    future_dates = pd.date_range(start=pd.to_datetime('today').replace(day=1), periods=n, freq='MS')
    future_days = (future_dates - df['idx_time'].min()).days
    
    # Dự đoán giá cho cả hai cổ phiếu
    predicted_AAA = np.polyval(coeffs_AAA, future_days)
    predicted_A32 = np.polyval(coeffs_A32, future_days)
    
    # Tạo DataFrame cho kết quả dự đoán
    future_df = pd.DataFrame({
        'idx_time': future_dates.strftime('%Y-%m'),  # Giữ định dạng tháng-năm
        'AAA': predicted_AAA,
        'A32': predicted_A32,
    })
    last_prediction = future_df.loc[len(future_df)-1]
    # print(last_prediction)
    result = {
        'idx_time': last_prediction['idx_time'],
        'AAA': last_prediction['AAA'],
        'A32': last_prediction['A32']
    }
    
    return json.dumps(result, default=str)

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
def get_api_portfolio(symbols):
    endday = datetime.now()
    startday = endday - timedelta(days=365)
    
    data = pd.DataFrame()
    for symbol in symbols:
        stock = Vnstock().stock(symbol=symbol, source='TCBS')
        try:
            df = stock.quote.history(start=startday.strftime('%Y-%m-%d'), 
                                     end=endday.strftime('%Y-%m-%d'), 
                                     interval='1D')
            if df.empty:
                return {"error": "No data found for symbol {}".format(symbol)}
            
            df['time'] = pd.to_datetime(df['time'])
            df = df.sort_values(by='time', ascending=False)
            
            df['month'] = df['time'].dt.month
            df['year'] = df['time'].dt.year
            
            df['idx_time'] = df['time'].dt.to_period('M')
                        
            df.set_index('idx_time', inplace=True)          
            df = df[['close']]
            df.columns = [symbol]
            data = pd.concat([data, df], axis=1)
        except Exception as e:
            return {"error": "Error for symbol {}: {}".format(symbol, str(e))}
    if data.empty:
        return {"error": "No data found for the given symbols and range"}
    
    data = data.groupby(data.index).mean()
    print(data)
    rets = np.log(data / data.shift(1)).dropna()
    
    result = rets.reset_index().to_dict(orient='records')
    
    return result

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
        HumanMessage("Hiện nay, một danh mục đầu tư của tôi bao gồm các mã cổ phiếu của sàn VNINDEX như là AAM, XPH, YEG, AAT. Tôi nên phân bổ vốn của mình như nào để tối ưu hóa danh mục đầu tư sao cho lợi nhuận được tối đa nhất trong chiến lược đầu tư dài hạn 6 tháng tới như thế nào? ", name="example_user"),
        AIMessage("", name="example_assistant", tool_calls=[{"name": "predict_future_prices", "args": {"symbols": ['AAM', 'XPH', 'YEG', 'AAT'], "n": 6}, "id": "1"}]),
        ToolMessage({'AAM':123, 'XPH':123, 'YEG':12, 'AAT':134}, tool_call_id="1"),
        AIMessage("", name="example_assistant", tool_calls=[{"name": "portfolio_optimize", "args": {"return": {'AAM':123, 'XPH':123, 'YEG':12, 'AAT':134}, "sharpe_ratio_or_variance": True}, "id": "2"}]),
        # AIMessage("", name="example_assistant", tool_calls=[{"name": "add", "args": {"x": 16505054784, "y": 4}, "id": "2"}]),
        ToolMessage({'AAM':0.25, 'XPH':0.25, 'YEG':0.25, 'AAT':0.25}, tool_call_id="2"),
        AIMessage("Có thể thấy, sau khi chạy mô hình dự đoán của hệ thống, tình hình cổ phiếu sẽ có sự biến động khá cao. Như vậy dựa vào kết quả dự đoán tình hình từng mã sau 6 tháng tới, bạn cần phân bố đều vốn cá nhân 25% ứng với mỗi loại cổ phiếu, để có được lợi nhuận cao nhất", name="example_assistant"),
    ],
    [
        HumanMessage("Hiện nay, một danh mục đầu tư của tôi bao gồm các mã cổ phiếu của sàn VNINDEX như là AAM, XPH, YEG, AAT. Tôi nên phân bổ vốn của mình như nào để tối ưu hóa danh mục đầu tư sao giảm thiểu rủi ro nhất trong chiến lược đầu tư dài hạn 6 tháng tới như thế nào? ", name="example_user"),
        AIMessage("", name="example_assistant", tool_calls=[{"name": "predict_future_prices", "args": {"symbols": ['AAM', 'XPH', 'YEG', 'AAT'], "n": 6}, "id": "1"}]),
        ToolMessage({'AAM':123, 'XPH':123, 'YEG':12, 'AAT':134}, tool_call_id="1"),
        AIMessage("", name="example_assistant", tool_calls=[{"name": "portfolio_optimize", "args": {"return": {'AAM':123, 'XPH':123, 'YEG':12, 'AAT':134}, "sharpe_ratio_or_variance": False}, "id": "2"}]),
        # AIMessage("", name="example_assistant", tool_calls=[{"name": "add", "args": {"x": 16505054784, "y": 4}, "id": "2"}]),
        ToolMessage({'AAM':0.15, 'XPH':-0.05, 'YEG':0.45, 'AAT':0.45}, tool_call_id="2"),
        AIMessage("Có thể thấy, sau khi chạy mô hình dự đoán của hệ thống, tình hình cổ phiếu sẽ có sự biến động khá cao. Như vậy dựa vào kết quả dự đoán tình hình từng mã sau 6 tháng tới, bạn cần phân bố đều vốn cá nhân lần lượt là, đầu tiên, rút 5% vốn hiện tại khỏi XPH, sử dụng 15% vốn vào AAM, 45% vốn cho cả YEG và AAT ứng với mỗi loại cổ phiếu, để có được lợi nhuận cao nhất", name="example_assistant"),
    ],
    [
        HumanMessage("Đánh giá công ty mã AAA có hoạt động ổn định hay không trong suốt 6 tháng qua, check lại sự kiện kèm tin tức để đánh giá mức độ của công ty."),
        AIMessage("Để đánh giá công ty, tôi sẽ kiểm tra các chỉ số tài chính chính của công ty trong 6 tháng qua và xem xét các sự kiện quan trọng, cũng như tin tức ảnh hưởng đến công ty. Hãy chờ trong giây lát..."),
        AIMessage("", name="example_assistant", tool_calls=[{"name": "get_company_information", "args": {"symbol": "AAA"}, "id": "1"}]),
        ToolMessage("", tool_call_id=1),
        AIMessage("Sau khi phân tích các chỉ số tài chính, xem xét các sự kiện và tin tức gần đây, công ty có vẻ hoạt động ổn định trong 6 tháng qua. Các yếu tố tài chính không cho thấy biến động lớn nào, và tin tức cũng không đề cập đến sự kiện nào gây ảnh hưởng nghiêm trọng.")
    ],
    [
        HumanMessage("Bạn hãy điều tra và tóm tắt về tiểu sử công ty mã A32 cùng với tình hình kinh doanh công ty trong suốt sáu tháng qua"),
        AIMessage("", name="example_assistant", tool_calls=[{"name": "multiply", "args": {"x": 3, "y": 2}, "id": "1"}]),
        ToolMessage("6", tool_call_id="1"),
        AIMessage("", name="example_assistant", tool_calls=[{"name": "add", "args": {"x": 5, "y": 6}, "id": "2"}]),
        ToolMessage("11", tool_call_id="2"),
        AIMessage("5 plus 3 times 2 is 11", name="example_assistant"),
    ],
    # [
    #     HumanMessage("Đánh giá công ty này có hoạt động ổn định hay không trong suốt 6 tháng quá, check lại sự kiện kèm tin tức để đánh giá mức độ của công ty"),
    #     AIMessage("", name="example_assistant", tool_calls=[{"name": "multiply", "args": {"x": 3, "y": 2}, "id": "1"}]),
    #     ToolMessage("6", tool_call_id="1"),
    #     AIMessage("", name="example_assistant", tool_calls=[{"name": "add", "args": {"x": 5, "y": 6}, "id": "2"}]),
    #     ToolMessage("11", tool_call_id="2"),
    #     AIMessage("5 plus 3 times 2 is 11", name="example_assistant"),
    # ],
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
