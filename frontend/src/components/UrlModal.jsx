import React from 'react'
import { Globe, Link, Search, BookOpen, MessageSquare, X, Zap, Database, HelpCircle } from 'lucide-react'

const UrlModal = ({ urlOptions, onClose, onAnalyzeNow, onAddToKnowledge, onAskQuestion }) => {
  if (!urlOptions.show) return null

  return (
    <div className="url-options-modal-overlay">
      <div className="url-options-modal">
        <div className="url-modal-header">
          <Globe size={16} />
          <h3>URL Detected</h3>
          <button onClick={onClose} className="close-modal-btn">
            <X size={16} />
          </button>
        </div>
        
        <div className="url-modal-content">
          <div className="url-preview">
            <Link size={12} />
            <span>{urlOptions.url}</span>
          </div>
          
          <p className="url-question">What would you like to do?</p>
          
          <div className="url-options-buttons">
            <button 
              onClick={onAnalyzeNow}
              className="url-option-btn primary"
              disabled={urlOptions.processing}
            >
              <Zap size={14} />
              <div className="url-option-text">
                <span className="url-option-title">Analyze Now</span>
                <span className="url-option-desc">Get immediate answer</span>
              </div>
            </button>
            
            <button 
              onClick={onAddToKnowledge}
              className="url-option-btn secondary"
              disabled={urlOptions.processing}
            >
              <Database size={14} />
              <div className="url-option-text">
                <span className="url-option-title">Add to Knowledge Base</span>
                <span className="url-option-desc">Permanent storage</span>
              </div>
            </button>

            <button 
              onClick={onAskQuestion}
              className="url-option-btn tertiary"
              disabled={urlOptions.processing}
            >
              <HelpCircle size={14} />
              <div className="url-option-text">
                <span className="url-option-title">Ask a Question</span>
                <span className="url-option-desc">Targeted analysis</span>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default UrlModal