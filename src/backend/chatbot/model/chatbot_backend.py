from typing import List, Tuple
from chatbot.utils.load_config import LoadProjectConfig
from chatbot.model.tools.load_tools_config import LoadToolsConfig
from chatbot.model.agent_graph.build_full_graph import build_graph
from chatbot.utils.app_utils import create_directory
from chatbot.utils.memory import Memory
# from chatbot.utils.langsmith_metrics import log_event
from chatbot.utils.langsmith_metrics import *
from datetime import datetime
URL = "https://github.com/Farzad-R/LLM-Zero-to-Hundred/tree/master/RAG-GPT"
hyperlink = f"[RAG-GPT user guideline]({URL})"

PROJECT_CFG = LoadProjectConfig()
TOOLS_CFG = LoadToolsConfig()

graph = build_graph()
config = {"configurable": {"thread_id": TOOLS_CFG.thread_id}}

create_directory("memory")


class ChatBot:
    """
    Lớp này chịu trách nhiệm xử lý các tương tác với chatbot bằng cách sử dụng một đồ thị tác nhân đã được định nghĩa trước.
    Chatbot tiếp nhận tin nhắn từ người dùng, sinh ra phản hồi thích hợp và lưu trữ lịch sử hội thoại vào thư mục bộ nhớ đã chỉ định.

    Thuộc tính:
        config (dict): Một từ điển cấu hình lưu trữ các thiết lập cụ thể như `thread_id`.

    Phương thức:
        respond(chatbot: List, message: str, userid: int) -> Tuple:
            Xử lý tin nhắn người dùng thông qua đồ thị tác nhân, sinh ra phản hồi,
            thêm phản hồi vào lịch sử hội thoại và lưu lịch sử hội thoại vào một tệp bộ nhớ.
    """
    @staticmethod
    def respond(chatbot: List, message: str, user_id:int) -> Tuple:
        """
        Xử lý một tin nhắn từ người dùng bằng cách sử dụng đồ thị tác nhân, sinh ra phản hồi và thêm phản hồi vào lịch sử hội thoại.
        Lịch sử hội thoại cũng được lưu vào một tệp bộ nhớ để tham khảo trong tương lai.

        Tham số:
            chatbot (List): Danh sách đại diện cho lịch sử hội thoại của chatbot.
                            Mỗi mục là một tuple gồm tin nhắn của người dùng và phản hồi của bot.
            message (str): Tin nhắn của người dùng để xử lý.

            user_id (int): Mã định danh của người dùng tham gia tương tác.

        Trả về:
            Tuple: Trả về một chuỗi rỗng (đại diện cho placeholder cho đầu vào mới của người dùng)
                   và lịch sử hội thoại đã được cập nhật.
        """
        events = graph.stream(
            {"messages": [("user", message)]}, config, stream_mode="values"
        )
        for event in events:
            event["messages"][-1].pretty_print()

        chatbot.append(
            (message, event["messages"][-1].content))
        response_content = event["messages"][-1].content
        # user_id = userid
        # log_event({
        #         "user_id": user_id,
        #         "user_query": message,
        #         "bot_response": response_content,
        #         "timestamp": datetime.now()
        #     })
        # Memory.write_chat_history_to_cache(
        #     gradio_chatbot=chatbot, thread_id=TOOLS_CFG.thread_id, user=userid
        # )
        Memory.save_chat_interaction(user=user_id, thread_id=TOOLS_CFG.thread_id, user_query=message, response=response_content)
        return "", chatbot
