from django.test import TestCase

# Create your tests here.
import unittest
import sys
import os
from django.contrib.auth import get_user_model
# import django
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'  

# django.setup()
from datetime import datetime
from typing import List, Tuple
from .utils.memory import Memory
from .model.chatbot_backend import ChatBot 
from .utils.load_config import LoadProjectConfig
from .model.tools.load_tools_config import LoadToolsConfig
# from model.tools.load_tools_config import LoadToolsConfig
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
PROJECT_CFG = LoadProjectConfig()
TOOLS_CFG = LoadToolsConfig()

class TestChatBot(TestCase):
    def setUp(self):
        User = get_user_model() 
        self.user = User.objects.create_user(username='testuser', password='password123', id=1)
        self.user_id = self.user.id  

        self.chatbot = []
        # self.message = "Xin chào chatbot!"
        self.messages = ["Xin chào chatbot!", "Năm 2024 có những sự kiện gì nổi bật đối với công ty mã A32?", "Hôm nay thời tiết như thế nào?", "Hiện nay, một danh mục đầu tư của tôi bao gồm các mã cổ phiếu của sàn VNINDEX như là AAA, A32 và risk free state là 0.01. Tôi nên phân bổ vốn của mình như nào để tối ưu hóa danh mục đầu tư sao cho lợi nhuận được tối đa nhất trong chiến lược đầu tư dài hạn 6 tháng tới như thế nào?", "Hãy tìm kiếm trên mạng, Vnstock là gì"]
        self.user_id = 1
        self.bot = ChatBot()

    def test_respond(self):
        # expected_response = ""  
        expected_responses = ["", "", "", "", ""]
        for i, message in enumerate(self.messages):
            response, updated_chatbot = self.bot.respond(self.chatbot, message, self.user_id)

            self.assertEqual(response, expected_responses[i], f"Unexpected response for message '{message}'")
            self.assertIn(message, [m[0] for m in updated_chatbot])
        # response, updated_chatbot = self.bot.respond(self.chatbot, self.message, self.user_id)

        # self.assertEqual(response, expected_response)
        # self.assertIn(self.message, [m[0] for m in updated_chatbot])

    def test_chat_history_saved(self):
        for message in self.messages:
            _, updated_chatbot = self.bot.respond(self.chatbot, message, self.user_id)

        chat_history = Memory.get_chat_history(self.user_id, TOOLS_CFG.thread_id)
        
        for message, response in zip(self.messages, [m[1] for m in updated_chatbot]):
            self.assertIn(message, [item[0] for item in chat_history])
            self.assertIn(response, [item[1] for item in chat_history])
        # _, updated_chatbot = self.bot.respond(self.chatbot, self.message, self.user_id)
        # chat_history = Memory.get_chat_history(self.user_id, TOOLS_CFG.thread_id)
        # print("chat đây",chat_history)
        
        # # self.assertIn(self.message, [item['user_query'] for item in chat_history])
        # # self.assertIn(updated_chatbot[-1][1], [item['response'] for item in chat_history])
        # self.assertIn(self.message, [item[0] for item in chat_history]) 
        # self.assertIn(updated_chatbot[-1][1], [item[1] for item in chat_history]) 

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

# python -m unittest test_chatbot.py
