import React, { useState, useEffect } from 'react'
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import Chat from './pages/chat'           // Majuscule
import Documents from './pages/Documents' // Majuscule
import Stats from './pages/Stats'         // Majuscule
import LandingPage from './pages/LandingPage'
import { useConversations } from './hooks/useConversations'
import './App.css'

function App() {
  const [darkMode, setDarkMode] = useState(false)
  const location = useLocation()
  const navigate = useNavigate()
  
  const {
    conversations,
    currentConversation,
    messages,
    saveMessages,
    newConversation,
    switchConversation,
    deleteConversation,
    clearMessages,
  } = useConversations()

  const isLandingPage = location.pathname === '/'

  useEffect(() => {
    const savedDarkMode = localStorage.getItem('darkMode') === 'true'
    setDarkMode(savedDarkMode)
  }, [])

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark-mode')
    } else {
      document.documentElement.classList.remove('dark-mode')
    }
    localStorage.setItem('darkMode', darkMode.toString())
  }, [darkMode])

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
  }

  const renderMainContent = () => {
    return (
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route 
          path="/chat" 
          element={
            <Chat 
              messages={messages}
              onSendMessage={saveMessages}
              onClearMessages={clearMessages}
            />
          } 
        />
        <Route path="/documents" element={<Documents />} />
        <Route 
          path="/stats" 
          element={<Stats conversations={conversations} />} 
        />
      </Routes>
    )
  }

  if (isLandingPage) {
    return (
      <div className="app">
        {renderMainContent()}
      </div>
    )
  }

  return (
    <div className="app">
      <Header darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
      
      <div className="container">
        <Sidebar 
          activeTab={location.pathname.substring(1) || 'chat'}
          setActiveTab={(tab) => navigate(`/${tab}`)}
          conversations={conversations}
          currentConversation={currentConversation}
          onNewConversation={newConversation}
          onSwitchConversation={switchConversation}
          onDeleteConversation={deleteConversation}
        />
        
        <main className="main-content">
          {renderMainContent()}
        </main>
      </div>
    </div>
  )
}

export default App