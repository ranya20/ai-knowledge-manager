import React from 'react'
import { MessageSquare, FolderOpen, BarChart3, Plus, Trash2 } from 'lucide-react'

const Sidebar = ({ 
  activeTab, 
  setActiveTab, 
  conversations, 
  currentConversation,
  onNewConversation,
  onSwitchConversation,
  onDeleteConversation
}) => {
  return (
    <aside className="sidebar">
      <button className="new-chat-btn" onClick={onNewConversation}>
        <Plus size={18} />
        New conversation
      </button>

      <div className="conversations-list">
        {conversations.length === 0 ? (
          <div className="no-conversations">
            <MessageSquare size={32} />
            <p>No conversations yet</p>
          </div>
        ) : (
          conversations.map(conv => (
            <div
              key={conv.id}
              className={`conversation-item ${currentConversation === conv.id ? 'active' : ''}`}
              onClick={() => onSwitchConversation(conv.id)}
            >
              <MessageSquare size={14} />
              <span className="conv-title">{conv.title}</span>
              <span className="conv-date">
                {new Date(conv.createdAt).toLocaleDateString()}
              </span>
              <button 
                className="delete-conversation-btn"
                onClick={(e) => {
                  e.stopPropagation()
                  onDeleteConversation(conv.id)
                }}
                title="Delete conversation"
              >
                <Trash2 size={14} />
              </button>
            </div>
          ))
        )}
      </div>

      <nav className="sidebar-nav">
        <button 
          className={`nav-item ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveTab('chat')}
        >
          <MessageSquare size={18} />
          Chat
        </button>
        <button 
          className={`nav-item ${activeTab === 'documents' ? 'active' : ''}`}
          onClick={() => setActiveTab('documents')}
        >
          <FolderOpen size={18} />
          Documents
        </button>
        <button 
          className={`nav-item ${activeTab === 'stats' ? 'active' : ''}`}
          onClick={() => setActiveTab('stats')}
        >
          <BarChart3 size={18} />
          Analytics
        </button>
      </nav>
    </aside>
  )
}

export default Sidebar