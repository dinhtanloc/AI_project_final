from langchain_core.tools import tool
from langchain_core.memory import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from chatbot.model.tools.load_tools_config import LoadToolsConfig

TOOLS_CFG = LoadToolsConfig()

class HistoryAgent:
    """
    Một công cụ để quản lý lịch sử hội thoại cho chatbot, cho phép ghi nhớ và xử lý các tin nhắn từ người dùng,
    giúp duy trì ngữ cảnh trong cuộc hội thoại.

    Công cụ này sử dụng mô hình ngôn ngữ để trả lời các câu hỏi từ người dùng dựa trên lịch sử hội thoại
    và các tin nhắn trước đó.

    Các thuộc tính:
        history_agent_llm (ChatOpenAI): Một phiên bản của mô hình ngôn ngữ ChatOpenAI được sử dụng để tạo phản hồi.
        chat_history (ChatMessageHistory): Lịch sử cuộc hội thoại, nơi lưu trữ các tin nhắn từ người dùng và phản hồi từ chatbot.
        system_role (str): Một mẫu nhắc hệ thống hướng dẫn mô hình ngôn ngữ trong việc trả lời các câu hỏi của người dùng.
        chain (RunnableWithMessageHistory): Một chuỗi các thao tác để quản lý lịch sử và tạo ra phản hồi cho người dùng.

    Các phương thức:
        __init__: Khởi tạo HistoryAgent với các cấu hình cần thiết.
    """

    def __init__(self, llm: str, llm_temperature: float, session_id: str) -> None:
        """
        Khởi tạo HistoryAgent với các cấu hình cần thiết.

        Tham số:
            llm (str): Tên của mô hình ngôn ngữ sẽ được sử dụng để tạo ra phản hồi.
            llm_temperature (float): Cài đặt nhiệt độ cho mô hình ngôn ngữ, kiểm soát độ ngẫu nhiên của phản hồi.
            session_id (str): ID phiên để quản lý lịch sử cuộc hội thoại.
        """
        self.history_agent_llm = ChatOpenAI(
            model=llm, temperature=llm_temperature)
        self.chat_history = ChatMessageHistory()
        self.system_role = """Given the following chat history and user question, generate a response.\n
            Chat History: {chat_history}\n
            User Question: {question}\n
            Response:
            """
        
        answer_prompt = PromptTemplate.from_template(self.system_role)
        self.chain = RunnableWithMessageHistory(
            answer_prompt | self.history_agent_llm | StrOutputParser(),
            lambda session_id: self.chat_history
        )
        self.session_id = session_id 

    def add_user_message(self, message: str):
        """Thêm tin nhắn của người dùng vào lịch sử cuộc hội thoại."""
        self.chat_history.add_user_message(message)

    def add_ai_message(self, message: str):
        """Thêm phản hồi của AI vào lịch sử cuộc hội thoại."""
        self.chat_history.add_ai_message(message)

    def invoke(self, question: str) -> str:
        """Gọi chuỗi để tạo phản hồi cho câu hỏi của người dùng."""
        response = self.chain.invoke({"question": question, "chat_history": self.chat_history.messages})
        return response


@tool
def chat_with_history(question: str, session_id: str) -> str:
    """Trả lời câu hỏi của người dùng với lịch sử cuộc hội thoại."""
    agent = HistoryAgent(
        llm=TOOLS_CFG.history_agent_llm,
        llm_temperature=TOOLS_CFG.history_agent_llm_temperature,
        session_id=session_id 
    )
    agent.add_user_message(question) 
    response = agent.invoke(question)
    agent.add_ai_message(response)  
    return response
