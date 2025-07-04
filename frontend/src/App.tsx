import { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ChatScreen from './components/ChatScreen';
import type { Conversation, Message } from './types/chat';
import { loadConversations, saveConversations } from './utils/storage';
import { sendMessage } from './utils/api';
import './App.css';

function App() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Load conversations from localStorage on mount
  useEffect(() => {
    const savedConversations = loadConversations();
    setConversations(savedConversations);
    
    // Set the most recent conversation as current, or create a new one if none exist
    if (savedConversations.length > 0) {
      const mostRecent = savedConversations.reduce((latest, current) => 
        current.updatedAt > latest.updatedAt ? current : latest
      );
      setCurrentConversationId(mostRecent.id);
    } else {
      createNewConversation();
    }
  }, []);

  // Save conversations to localStorage whenever they change
  useEffect(() => {
    if (conversations.length > 0) {
      saveConversations(conversations);
    }
  }, [conversations]);

  const createNewConversation = () => {
    const newConversation: Conversation = {
      id: Date.now().toString(),
      title: 'New Conversation',
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    
    setConversations(prev => [newConversation, ...prev]);
    setCurrentConversationId(newConversation.id);
  };

  const getCurrentConversation = (): Conversation | null => {
    return conversations.find(conv => conv.id === currentConversationId) || null;
  };

  const updateConversationTitle = (conversationId: string, firstMessage: string) => {
    const title = firstMessage.length > 30 
      ? firstMessage.substring(0, 30) + '...' 
      : firstMessage;
    
    setConversations(prev => prev.map(conv => 
      conv.id === conversationId 
        ? { ...conv, title, updatedAt: new Date() }
        : conv
    ));
  };

  const addMessageToConversation = (conversationId: string, message: Message) => {
    setConversations(prev => prev.map(conv => {
      if (conv.id === conversationId) {
        const updatedMessages = [...conv.messages, message];
        return {
          ...conv,
          messages: updatedMessages,
          updatedAt: new Date(),
        };
      }
      return conv;
    }));
  };

  const handleSendMessage = async (content: string) => {
    if (!currentConversationId) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      timestamp: new Date(),
      isUser: true,
    };

    // Add user message immediately
    addMessageToConversation(currentConversationId, userMessage);

    // Update conversation title if it's the first message
    const currentConversation = getCurrentConversation();
    if (currentConversation && currentConversation.messages.length === 0) {
      updateConversationTitle(currentConversationId, content);
    }

    setIsLoading(true);

    try {
      // Send message to API
      const response = await sendMessage(content);

      // Add AI response
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response,
        timestamp: new Date(),
        isUser: false,
      };

      addMessageToConversation(currentConversationId, aiMessage);
    } catch (error) {
      console.error('Failed to send message:', error);
      
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
        isUser: false,
      };

      addMessageToConversation(currentConversationId, errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectConversation = (conversationId: string) => {
    setCurrentConversationId(conversationId);
  };

  const currentConversation = getCurrentConversation();

  return (
    <div className="app">
      <Header />
      <div className="main-content">
        <Sidebar
          conversations={conversations}
          currentConversationId={currentConversationId}
          onNewConversation={createNewConversation}
          onSelectConversation={handleSelectConversation}
        />
        <ChatScreen
          messages={currentConversation?.messages || []}
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
}

export default App;
