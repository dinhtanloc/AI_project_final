import os
import pandas as pd
from typing import List
from datetime import datetime, date
from chatbot.models import ChatHistory  

class Memory:
    """
    Một lớp để xử lý việc lưu trữ lịch sử hội thoại của chatbot bằng cách lưu tạm thời các tin nhắn vào bộ nhớ đệm (cache) 
    và sau đó ghi chúng vào cơ sở dữ liệu.

    Thuộc tính:
        cache (List[Dict]): Bộ nhớ tạm thời lưu các tin nhắn chưa được ghi vào cơ sở dữ liệu.

    Phương thức:
        write_chat_history_to_cache(gradio_chatbot: List, thread_id: str, user) -> None:
            Lưu tương tác mới nhất của chatbot (truy vấn của người dùng và phản hồi của bot) vào bộ nhớ tạm thời (cache).
            Mỗi tương tác bao gồm thông tin về mã luồng, truy vấn của người dùng, phản hồi từ chatbot, và dấu thời gian.

        save_cache_to_database() -> None:
            Ghi toàn bộ các tin nhắn từ bộ nhớ đệm (cache) vào cơ sở dữ liệu và xóa bộ nhớ đệm sau khi hoàn thành.
    """

    cache = []  

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
            Memory.cache.clear()
