import os
import pandas as pd
from typing import List
from datetime import datetime, date
from chatbot.models import ChatHistory
from accounts.models import User
from chatbot.model.utils.prepare_vectodb import PrepareVectorDB
from chatbot.model.config.load_tools_config import TOOLS_CFG
class Memory:
    """
        Lớp này chịu trách nhiệm xử lý việc lưu trữ lịch sử hội thoại của chatbot.
        Nó thực hiện việc lưu trữ tạm thời các tin nhắn vào bộ nhớ đệm (cache)
        và sau đó ghi chúng vào cơ sở dữ liệu để theo dõi và phân tích.

        Thuộc tính:
            cache (List[Dict]): Bộ nhớ tạm thời lưu trữ các tin nhắn chưa được ghi vào cơ sở dữ liệu,
                                mỗi tin nhắn bao gồm thông tin về người dùng, mã luồng, truy vấn và phản hồi.

        Phương thức:
            save_chat_interaction(user, thread_id: str, user_query: str, response: str) -> None:
                Lưu lại một tương tác mới nhất của chatbot (truy vấn của người dùng và phản hồi của bot) vào cơ sở dữ liệu.
                Mỗi bản ghi lưu trữ thông tin về người dùng, mã luồng, truy vấn, phản hồi và thời gian tương tác.

            write_chat_history_to_cache(gradio_chatbot: List, thread_id: str, user) -> None:
                Lưu lại tương tác mới nhất của chatbot (truy vấn của người dùng và phản hồi của bot) vào bộ nhớ tạm thời (cache).
                Mỗi bản ghi bao gồm thông tin về người dùng, mã luồng, truy vấn, phản hồi và thời gian tương tác.

            save_cache_to_database() -> None:
                Ghi tất cả các tin nhắn từ bộ nhớ tạm thời (cache) vào cơ sở dữ liệu.
                Sau khi ghi xong, bộ nhớ tạm thời sẽ được xóa để giải phóng bộ nhớ.
      """
    cache = []
    vectodb=PrepareVectorDB(
                doc_dir='',
                chunk_size=500,
                chunk_overlap=100,
                mongodb_uri=TOOLS_CFG.admin_rag_mongodb_url,
                db_name=TOOLS_CFG.history_rag_db_name, 
                collection_name=TOOLS_CFG.history_rag_collection_name,  
            )

    @staticmethod
    def write_chat_history_to_cache(gradio_chatbot: List, thread_id: str, user) -> None:
        """
        Lưu lại tương tác mới nhất của chatbot (truy vấn của người dùng và phản hồi) vào bộ nhớ tạm thời (cache).
        Mỗi bản ghi bao gồm mã luồng, người dùng, truy vấn, phản hồi, và dấu thời gian.

        Tham số:
            gradio_chatbot (List): Danh sách chứa các cặp (truy vấn của người dùng, phản hồi của chatbot).
                                   Tương tác mới nhất được lấy từ cuối danh sách.
            thread_id (str): Mã định danh duy nhất cho phiên trò chuyện.
            user: Người dùng đang tham gia phiên trò chuyện.

        Trả về:
            None
        """
        user_query, response = gradio_chatbot[-1]
        Memory.cache.append({
            'user': user,
            'thread_id': thread_id,
            'user_query': user_query,
            'response': response,
            'timestamp': datetime.now()
        })

    @staticmethod
    def save_cache_to_database():
        """
        Ghi tất cả các tin nhắn từ bộ nhớ tạm thời (cache) vào cơ sở dữ liệu. Sau khi ghi, bộ nhớ tạm thời được xóa.

        Trả về:
            None
        """
        if Memory.cache:
            ChatHistory.objects.bulk_create([
                ChatHistory(
                    user=item['user'],
                    thread_id=item['thread_id'],
                    user_query=item['user_query'],
                    response=item['response'],
                    timestamp=item['timestamp']
                )
                for item in Memory.cache
            ])
            for item in Memory.cache:
                Memory.vectodb.save_history_response_vectodb(userid=item['user'], response=item['response'])

            Memory.cache.clear()


    @staticmethod
    def save_chat_interaction(user, thread_id: str, user_query: str, response: str) -> None:
        """
        Lưu lại tương tác mới nhất của chatbot vào cơ sở dữ liệu.
        Mỗi bản ghi bao gồm mã luồng, người dùng, truy vấn, phản hồi, và dấu thời gian.

        Tham số:
            user: Người dùng đang tham gia phiên trò chuyện.
            thread_id (str): Mã định danh duy nhất cho phiên trò chuyện.
            user_query (str): Truy vấn của người dùng.
            response (str): Phản hồi từ chatbot.

        Trả về:
            None
        """
        print(f"Saving chat interaction: User: {user}, Thread ID: {thread_id}, Query: {user_query}, Response: {response}")
        # user_instance = User.objects.get(id=user)
        try:
            user_instance = User.objects.get(id=user)
        except User.DoesNotExist:
            print(f"User with id {user} does not exist.")
            return  
        chat_history = ChatHistory(
            user=user_instance,
            thread_id=thread_id,
            user_query=user_query,
            response=response,
            timestamp=datetime.now()
        )
        chat_history.save()
        Memory.vectodb.save_history_response_vectodb(userid=user, response=response)

    @staticmethod
    def get_chat_history(user, thread_id: str) -> List:
        """
        Truy xuất lịch sử hội thoại của người dùng từ cơ sở dữ liệu.

        Tham số:
            user: Người dùng yêu cầu lịch sử hội thoại.
            thread_id (str): Mã định danh của phiên trò chuyện.

        Trả về:
            List: Danh sách các tin nhắn trong lịch sử hội thoại.
        """
        history = ChatHistory.objects.filter(user=user, thread_id=thread_id).order_by('timestamp')
        return [(entry.user_query, entry.response) for entry in history]

    @staticmethod
    def save_chat_history_periodically(interval: int) -> None:
        """
        Tự động lưu cache vào cơ sở dữ liệu sau mỗi khoảng thời gian nhất định.

        Tham số:
            interval (int): Khoảng thời gian giữa các lần lưu (tính bằng giây).
        """
        import time
        while True:
            Memory.save_cache_to_database()
            time.sleep(interval)