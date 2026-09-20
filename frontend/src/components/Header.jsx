import React from 'react'
import { Brain, Moon, Sun, Sparkles } from 'lucide-react'

const Header = ({ darkMode, toggleDarkMode }) => {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo-container">
          <Brain size={28} className="logo" color="#FF8A00" />
        </div>
        <div className="header-text">
          <h1>StudyMind AI</h1>
          <p>Ask questions about your documents and URLs</p>
        </div>
        <button 
          onClick={toggleDarkMode}
          className="theme-toggle"
          title={darkMode ? 'Light mode' : 'Dark mode'}
        >
          {darkMode ? <Sun size={18} /> : <Moon size={18} />}
        </button>
      </div>
    </header>
  )
}

export default Header