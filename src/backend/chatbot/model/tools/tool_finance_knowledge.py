from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
import datetime
from langchain_core.prompts import ChatPromptTemplate
from .finance_toollists import tool_mapping, tools
from .load_tools_config import LoadToolsConfig

TOOLS_CFG = LoadToolsConfig()

class FinanceAgent:
    """
    SQLAgent với few-shot prompting cho phép mô hình học hỏi từ một vài ví dụ về các truy vấn SQL
    và cách trả lời trước khi đưa ra câu trả lời cuối cùng.
    """

    def __init__(self, llm: str, ques: str, llm_temperature: float, tools ) -> None:
        """
        Khởi tạo SQLAgent với các cấu hình cần thiết.

        Tham số:
            llm (str): Tên của mô hình ngôn ngữ sẽ được sử dụng để tạo ra và diễn giải các truy vấn SQL.
            ques (str): Câu hỏi được đưa ra để tìm kiếm thông tin.
            llm_temperature (float): Cài đặt nhiệt độ cho mô hình ngôn ngữ, kiểm soát độ ngẫu nhiên của phản hồi.
        """

        self.llm = ChatOpenAI(
            model=llm, temperature=llm_temperature)
        self.sql_agent_llm=self.llm.bind_tools(tools)
        # Few-shot prompt examples
        self.examples = [


            HumanMessage(content="Hiện nay, một danh mục đầu tư của tôi bao gồm các mã cổ phiếu của sàn VNINDEX như là AAA, A32 và risk free state là 0.01. Tôi nên phân bổ vốn của mình như nào để tối ưu hóa danh mục đầu tư sao cho lợi nhuận được tối đa nhất trong chiến lược đầu tư dài hạn 6 tháng tới như thế nào?", name="example_user1"),
            AIMessage(content="", name="example_assistant1", tool_calls=[{"name": "get_api_portfolio", "args": {"symbols": ['AAA', 'A32'], "n": 6}, "id": "1"}]),
            ToolMessage(content='[{"idx_time": "2023-09", "AAA": -0.05144315555216674, "A32": 0.0884884106784579}, {"idx_time": "2023-10", "AAA": -0.14542232114660703, "A32": -0.0963458098223358}, {"idx_time": "2023-11", "AAA": 0.022231032778677464, "A32": 0.03697967078334708}, {"idx_time": "2023-12", "AAA": 0.03516170679547651, "A32": 0.031034356695593013}, {"idx_time": "2024-01", "AAA": 0.03523565930437369, "A32": 0.0753295051569786}, {"idx_time": "2024-02", "AAA": 0.11900386259347105, "A32": 0.3768284474520035}, {"idx_time": "2024-03", "AAA": -0.003568951221208245, "A32": -0.2758677123166095}, {"idx_time": "2024-04", "AAA": -0.043706234983660705, "A32": 0.08584764872201436}, {"idx_time": "2024-05", "AAA": 0.06614997833044046, "A32": -0.17193531125845293}, {"idx_time": "2024-06", "AAA": 0.027219402108996846, "A32": 0.04964901833003382}, {"idx_time": "2024-07", "AAA": 0.023138676922500895, "A32": -0.003968290420115657}, {"idx_time": "2024-08", "AAA": -0.1058755282870188, "A32": 0.05798319264886414}]', tool_call_id="1"),
            AIMessage(content="", name="example_assistant1", tool_calls=[{"name": "predict_future_prices", "args": {"symbols": ['AAM', 'XPH', 'YEG', 'AAT'], "n": 6}, "id": "2"}]),
            ToolMessage(content='{"AAA": -0.4000549560521612, "A32": -0.020533696676693372}', tool_call_id="2"),
            AIMessage(content="", name="example_assistant1", tool_calls=[{"name": "portfolio_optimize", "args": {"returns": {"AAA": -0.4000549560521612, "A32": -0.020533696676693372}, "sharpe_ratio_or_variance": True,"risk_free_rate":0.01}, "id": "3"}]),
            ToolMessage(content="{'AAA': 0.5, 'A32': 0.5}", tool_call_id="3"),
            AIMessage(content="Có thể thấy, sau khi chạy mô hình dự đoán của hệ thống, tình hình cổ phiếu sẽ có sự biến động khá cao. Như vậy dựa vào kết quả dự đoán tình hình từng mã sau 6 tháng tới, bạn cần phân bố đều vốn cá nhân 50% ứng với mỗi loại cổ phiếu, để có được lợi nhuận cao nhất", name="example_assistant1"),

        ]
        # Prompt Template for few-shot
        self.system_role = f"""Bạn là một chuyên gia chơi chứng khoán trong lĩnh vực kinh tế đầu tư tại thị trường chứng khoán Việt Nam. Hôm nay là ngày {datetime.now().strftime('%Y-%m-%d')}. Sử dụng các tool được cung cấp như một ví dụ để đưa ra những lời khuyên hữu ích để người chơi mới tại Việt Nam lựa chọn và tối ưu hóa danh mục đầu tư, đầu tư chứng khoán thành công
        """

        few_shot_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_role),
                *self.examples,
                ("human", "{query}"),
            ]

        )


        self.chain = {"query": RunnablePassthrough()} | few_shot_prompt | self.sql_agent_llm | StrOutputParser()




@tool
def query_stock_logic(ques: str) -> str:
    """Truy vấn dữ liệu thị trường chứng khoán Việt Nam từ cơ sở dữ liệu SQL Vnstock với hỗ trợ few-shot prompting."""
    messages = [HumanMessage(ques)]
    agent = FinanceAgent(
        llm=TOOLS_CFG.sqlagent_llm,
        sqldb_directory=TOOLS_CFG.sqldb_directory,
        llm_temerature=TOOLS_CFG.sqlagent_llm_temperature,
        tools=tools
    )
    ai_msg = agent.chain.invoke(ques)
    messages.append(ai_msg)
    for tool_call in ai_msg.tool_calls:
        print(tool_call)
        selected_tool = tool_mapping[tool_call["name"].lower()]
        print(tool_call["args"])
        tool_output = selected_tool.invoke(dict(tool_call["args"]))
        print(type(tool_output), tool_output)
        messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))
    response =agent.chain.invoke(messages).content
    return response