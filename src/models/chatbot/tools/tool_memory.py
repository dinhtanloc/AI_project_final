from langchain_core.tools import tool
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from config.load_tools_config import TOOLS_CFG
import pymongo
import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())


class HistoryAgent:
    """
    Quản lý lịch sử hội thoại cho chatbot, ghi nhớ và xử lý tin nhắn từ người dùng để duy trì ngữ cảnh.

    Thuộc tính:
        history_agent_llm (ChatOpenAI): Mô hình ngôn ngữ dùng để tạo phản hồi.
        chat_history (ChatMessageHistory): Lưu trữ tin nhắn từ người dùng và phản hồi từ chatbot.
        system_role (str): Mẫu nhắc hướng dẫn mô hình trong việc trả lời câu hỏi.
        chain (RunnableWithMessageHistory): Chuỗi thao tác để quản lý lịch sử và tạo phản hồi.

    Phương thức:
        __init__: Khởi tạo với cấu hình cần thiết.
    """

    def __init__(self, llm: str, llm_temperature: float, thread_id: str) -> None:
        """
        Khởi tạo HistoryAgent với các cấu hình cần thiết.

        Tham số:
            llm (str): Tên của mô hình ngôn ngữ sẽ được sử dụng để tạo ra phản hồi.
            llm_temperature (float): Cài đặt nhiệt độ cho mô hình ngôn ngữ, kiểm soát độ ngẫu nhiên của phản hồi.
            thread_id (str): Mã phiên để theo dõi và quản lý lịch sử hội thoại của người dùng.
          
        """
        self.name='chat_with_history'
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
            lambda thread_id: self.chat_history
        )
        self.thread_id = thread_id

      
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
    
  


@tool('chat_with_history')
def chat_with_history(query: str,user_id:str, thread_id: str) -> str:
    """Trả lời câu hỏi của người dùng với lịch sử cuộc hội thoại, tìm kiếm nhanh."""
    agent = HistoryAgent(
        llm=TOOLS_CFG.history_agent_llm,
        llm_temperature=TOOLS_CFG.history_agent_llm_temperature,
        thread_id=thread_id,
    )
    agent.add_user_message(query) 
    response = agent.invoke(query)
    agent.add_ai_message(response)  
    return response


