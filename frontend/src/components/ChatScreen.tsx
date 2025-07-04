import React, { useState, useRef, useEffect } from 'react';
import type { Message } from '../types/chat';

interface ChatScreenProps {
  messages: Message[];
  onSendMessage: (message: string) => void;
  isLoading?: boolean;
}

const ChatScreen: React.FC<ChatScreenProps> = ({ messages, onSendMessage, isLoading = false }) => {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue.trim());
      setInputValue('');
    }
  };

  const formatTime = (date: Date): string => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chat-screen">
      {/* Messages Area */}
      <div className="messages-area">
        {messages.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-content">
              <div className="empty-state-icon">💬</div>
              <p className="empty-state-title">Start a new conversation</p>
              <p className="empty-state-subtitle">I'm an AI soda machine!</p>
              <p className="empty-state-subtitle">You can ask me anything or order, for example:</p><br></br>
              <p className="empty-state-subtitle">What do you have in stock?</p> <br></br>
              <p className="empty-state-subtitle">I want to buy a coke</p>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.isUser ? 'user' : 'ai'}`}
            >
              <div className="message-content">
                <div>{message.content}</div>
                <div className="message-time">
                  {formatTime(message.timestamp)}
                </div>
              </div>
            </div>
          ))
        )}
        
        {isLoading && (
          <div className="loading-message">
            <div className="loading-content">
              <div className="loading-dots">
                <div className="loading-dot"></div>
                <div className="loading-dot"></div>
                <div className="loading-dot"></div>
              </div>
              <span>AI is thinking...</span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="input-area">
        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your message..."
            disabled={isLoading}
            className="message-input"
          />
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="send-button"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatScreen; 