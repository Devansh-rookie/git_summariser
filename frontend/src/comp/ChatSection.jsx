import React, { useState } from 'react';
import { MessageSquare, Send } from 'lucide-react';

const ChatSection = ({ initialMessages, selectedFileName }) => {
  const [chatMessages, setChatMessages] = useState(initialMessages);
  const [inputMessage, setInputMessage] = useState('');

  const handleSendMessage = () => {
    if (inputMessage.trim() === '') return;
    
    setChatMessages([
      ...chatMessages,
      { role: 'user', content: inputMessage },
    ]);
    
    // Simulate AI response
    setTimeout(() => {
      setChatMessages(prev => [
        ...prev,
        { 
          role: 'assistant', 
          content: `I see you're working with React components. The code in ${selectedFileName} looks good, but you might want to consider extracting the button logic into a separate function for better readability.` 
        },
      ]);
    }, 1000);
    
    setInputMessage('');
  };

  return (
    <div className="h-1/2 flex flex-col">
      <div className="p-3 border-b border-[#21262d] font-semibold flex items-center">
        <MessageSquare size={18} className="mr-2 text-[#58a6ff]" />
        AI Assistant
      </div>
      <div className="flex-grow overflow-y-auto p-4 space-y-4">
        {chatMessages.map((message, index) => (
          <div 
            key={index} 
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div 
              className={`max-w-3/4 p-3 rounded-lg shadow-md ${
                message.role === 'user' 
                  ? 'bg-[#238636] text-white' 
                  : 'bg-[#161b22] text-gray-200 border border-[#30363d]'
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
      </div>
      <div className="p-3 border-t border-[#21262d]">
        <div className="flex items-center">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Ask about your code..."
            className="flex-grow bg-[#161b22] text-gray-200 p-2 rounded-l-md focus:outline-none focus:ring-1 focus:ring-[#58a6ff] border border-[#30363d] border-r-0 transition-all"
          />
          <button 
            onClick={handleSendMessage}
            className="bg-[#238636] p-2 rounded-r-md hover:bg-[#2ea043] transition-colors"
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatSection;