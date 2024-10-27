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
from chatbot.model.tools.load_tools_config import LoadToolsConfig
import pymongo
import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

TOOLS_CFG = LoadToolsConfig()

class HistoryMongoDBAgent:
    """
    Quản lý lịch sử hội thoại cho chatbot sử dụng mongoDB, ghi nhớ và xử lý tin nhắn từ người dùng để duy trì ngữ cảnh.

    Thuộc tính:
        history_agent_llm (ChatOpenAI): Mô hình ngôn ngữ dùng để tạo phản hồi.
        chat_history (ChatMessageHistory): Lưu trữ tin nhắn từ người dùng và phản hồi từ chatbot.
        system_role (str): Mẫu nhắc hướng dẫn mô hình trong việc trả lời câu hỏi.
        chain (RunnableWithMessageHistory): Chuỗi thao tác để quản lý lịch sử và tạo phản hồi.

    Phương thức:
        __init__: Khởi tạo với cấu hình cần thiết.
    """

    def __init__(self, llm: str, llm_temperature: float, user_id: str, thread_id: str, mongodb_uri: str, db_name: str, collection_name: str) -> None:
        """
        Khởi tạo HistoryAgent với các cấu hình cần thiết.

        Tham số:
            llm (str): Tên của mô hình ngôn ngữ sẽ được sử dụng để tạo ra phản hồi.
            llm_temperature (float): Cài đặt nhiệt độ cho mô hình ngôn ngữ, kiểm soát độ ngẫu nhiên của phản hồi.
            thread_id (str): Mã phiên để theo dõi và quản lý lịch sử hội thoại của người dùng.
            user_id (str): ID người dùng để check database.
            mongodb_uri (str): URI kết nối đến cơ sở dữ liệu MongoDB.
            db_name (str): Tên cơ sở dữ liệu MongoDB mà HistoryAgent sẽ sử dụng.
            collection_name (str): Tên bộ sưu tập (collection) trong cơ sở dữ liệu MongoDB để lưu trữ lịch sử hội thoại.
        """
        self.name='chat_with_history'
        self.history_agent_llm = ChatOpenAI(
            model=llm, temperature=llm_temperature)
        self.chat_history = ChatMessageHistory()
        self.user_id=user_id
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

        try:
            self.client = pymongo.MongoClient(mongodb_uri)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            print("Connection to MongoDB successful")
        except pymongo.errors.ConnectionFailure as e:
            print(f"Connection failed: {e}")

    def add_user_message(self, message: str):
        """Thêm tin nhắn của người dùng vào lịch sử cuộc hội thoại."""
        self.chat_history.add_user_message(message)
        self.save_to_mongodb(self.user_id, message, is_user_message=True)

    def add_ai_message(self, message: str):
        """Thêm phản hồi của AI vào lịch sử cuộc hội thoại."""
        self.chat_history.add_ai_message(message)
        self.save_to_mongodb(self.user_id, message, is_user_message=False)

    def invoke(self, question: str) -> str:
        """Gọi chuỗi để tạo phản hồi cho câu hỏi của người dùng."""
        response = self.chain.invoke({"question": question, "chat_history": self.chat_history.messages})
        return response
    
    def save_to_mongodb(self, message: str, is_user_message: bool):
        """Lưu tin nhắn vào MongoDB."""
        try:
            vector = self.embedding_model.encode(message).tolist()
            document = {
                "user_id": self.user_id,
                "thread_id": self.thread_id,
                "message": message,
                "is_user_message": is_user_message,
                "vector": vector
            }
            self.collection.insert_one(document)
        except Exception as e:
            print(f"Lỗi khi lưu vào MongoDB: {e}")


    def similarity_search(self, query: str, k: int = None):
        """Thực hiện tìm kiếm tin nhắn tương tự bằng cách sử dụng truy vấn từ người dùng."""
        query_vector = self.embedding_model.encode(query).tolist()

        if query_vector is None:
            return "Invalid query or embedding generation failed."

        if k is None:
            k = 5  # Hoặc một giá trị mặc định khác

        vector_search_stage = {
            "$vectorSearch": {
                "index": "vector_index", 
                "queryVector": query_vector,
                "path": "vector", 
                "numCandidates": 400,
                "limit": k,
            }
        }

        project_stage = {
            "$project": {
                "_id": 0,
                "message": 1,
                "score": {
                    "$meta": "vectorSearchScore"
                }
            }
        }

        pipeline = [vector_search_stage, project_stage]
        try:
            results = list(self.collection.aggregate(pipeline))
            return results
        except Exception as e:
            print(e)
            return []



@tool('chat_with_history_with_db_using_mongodb')
def chat_with_history_with_db_using_mongodb(query: str,user_id:str, thread_id: str) -> str:
    """Dựa câu hỏi của người dùng với lịch sử cuộc hội thoại, sử dụng database mongodb, truy xuất đoạn hội thoại liên quan từ database dựa trên phiên trò chuyện thread_id và user_id, nếu trong trường hợp hàm chat_with_history tìm ko ra."""
    agent = HistoryMongoDBAgent(
        llm=TOOLS_CFG.history_agent_llm,
        llm_temperature=TOOLS_CFG.history_agent_llm_temperature,
        thread_id=thread_id,
        mongodb_uri=os.getenv('MONGODB_URL'), 
        user_id=user_id,
        db_name=TOOLS_CFG.history_rag_db_name,  
        collection_name=TOOLS_CFG.history_rag_collection_name
    )
    agent.add_user_message(query) 
    similar_messages = agent.similarity_search(query)
    
    combined_query = f"{query}\n\nTin nhắn tương tự:\n" + "\n".join([msg['message'] for msg in similar_messages])
    
    response = agent.invoke(combined_query)
    agent.add_ai_message(response)
    return response
