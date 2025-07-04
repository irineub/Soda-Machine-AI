import React from 'react';
import type { Conversation } from '../types/chat';

interface SidebarProps {
  conversations: Conversation[];
  currentConversationId: string | null;
  onNewConversation: () => void;
  onSelectConversation: (conversationId: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  conversations,
  currentConversationId,
  onNewConversation,
  onSelectConversation,
}) => {
  const formatDate = (date: Date): string => {
    const now = new Date();
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);
    
    if (diffInHours < 24) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else {
      return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
    }
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <button
          onClick={onNewConversation}
          className="new-conversation-btn"
        >
          New Conversation
        </button>
      </div>
      
      <div className="sidebar-content">
        <h3 className="sidebar-title">Conversation History</h3>
        {conversations.length === 0 ? (
          <p className="no-conversations">No conversations yet</p>
        ) : (
          <div className="conversation-list">
            {conversations.map((conversation) => (
              <button
                key={conversation.id}
                onClick={() => onSelectConversation(conversation.id)}
                className={`conversation-item ${
                  currentConversationId === conversation.id ? 'active' : ''
                }`}
              >
                <div className="conversation-title">
                  {conversation.title}
                </div>
                <div className="conversation-date">
                  {formatDate(conversation.updatedAt)}
                </div>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar; 