import unittest
import sys
import os
import django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'  

django.setup()
from datetime import datetime
from models.utils.memory import Memory
from typing import List, Tuple
from chatbot.model.chatbot_backend import ChatBot 
from chatbot.utils.load_config import LoadProjectConfig
from chatbot.model.config.load_tools_config import LoadToolsConfig
# from model.tools.load_tools_config import LoadToolsConfig
from django.test import TestCase
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
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
        print("chat đây",chat_history)
        
        # self.assertIn(self.message, [item['user_query'] for item in chat_history])
        # self.assertIn(updated_chatbot[-1][1], [item['response'] for item in chat_history])
        self.assertIn(self.message, [item[0] for item in chat_history]) 
        self.assertIn(updated_chatbot[-1][1], [item[1] for item in chat_history]) 

if __name__ == "__main__":
    unittest.main()


# python -m unittest test_chatbot.py
