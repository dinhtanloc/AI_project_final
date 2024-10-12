import unittest
import sys
import os
import django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'  # Thay your_project.settings bằng đường dẫn tới settings.py của bạn

# # Khởi tạo Django
django.setup()
from datetime import datetime
from chatbot.utils.memory import Memory
from typing import List, Tuple
from chatbot.model.chatbot_backend import ChatBot 
from chatbot.utils.load_config import LoadProjectConfig
from chatbot.model.tools.load_tools_config import LoadToolsConfig
# from model.tools.load_tools_config import LoadToolsConfig
from django.test import TestCase

PROJECT_CFG = LoadProjectConfig()
TOOLS_CFG = LoadToolsConfig()

class TestChatBot(TestCase):
    def setUp(self):
        self.chatbot = []
        self.message = "Xin chào chatbot!"
        self.user_id = 1
        self.bot = ChatBot()

    def test_respond(self):
        expected_response = ""  
        response, updated_chatbot = self.bot.respond(self.chatbot, self.message, self.user_id)

        self.assertEqual(response, expected_response)
        self.assertIn(self.message, [m[0] for m in updated_chatbot])

    def test_chat_history_saved(self):
        _, updated_chatbot = self.bot.respond(self.chatbot, self.message, self.user_id)
        chat_history = Memory.get_chat_history(self.user_id, TOOLS_CFG.thread_id)
        
        self.assertIn(self.message, [item['user_query'] for item in chat_history])
        self.assertIn(updated_chatbot[-1][1], [item['response'] for item in chat_history])

if __name__ == "__main__":
    

    # print(os.path.dirname(os.path.abspath(__file__)) + '/../')

    unittest.main()


# python -m unittest test_chatbot.py
