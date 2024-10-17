import React from 'react';
import Sidebar from '@client/components/ChatbotSidebar/Sidebar';
import Chatbot from '@client/components/UI/Chatbot'
import '@client/styles/chatbotpage.css'
const ChatbotPage = () => {
  return (
    <div className="chatbot-page-container">
      <Sidebar/>
      <Chatbot/>
      </div>
  )
}

export default ChatbotPage;
