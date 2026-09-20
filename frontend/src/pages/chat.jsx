import React, { useState, useEffect, useRef } from 'react'
import { Send, Trash2, User, Bot, Brain, Globe, Link, Sparkles, Zap, Cpu } from 'lucide-react'
import { chatAPI } from '../services/api'
import UrlModal from '../components/UrlModal'
import robotImage from '../../ai.png'

const Chat = ({ messages, onSendMessage, onClearMessages }) => {
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [urlOptions, setUrlOptions] = useState({
    show: false,
    url: '',
    processing: false
  })
  
  const messagesEndRef = useRef(null)

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const isUrl = (text) => {
    const urlRegex = /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/
    return urlRegex.test(text.trim())
  }

  const handleSendMessage = async (e) => {
    e.preventDefault()
    if (!inputMessage.trim() || isLoading) return

    if (isUrl(inputMessage)) {
      setUrlOptions({
        show: true,
        url: inputMessage,
        processing: false
      })
      return
    }

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    }

    const newMessages = [...messages, userMessage]
    onSendMessage(newMessages)
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await chatAPI.ask(inputMessage)
      
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.data.answer,
        sources: response.data.sources || [],
        timestamp: new Date().toISOString()
      }

      onSendMessage([...newMessages, botMessage])
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: 'Error: ' + (error.response?.data?.error || error.message),
        timestamp: new Date().toISOString()
      }
      onSendMessage([...newMessages, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const processUrlImmediate = async (url, question = '') => {
    setUrlOptions(prev => ({ ...prev, processing: true }))
    
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: `URL: ${url}${question ? `\n\nQuestion: ${question}` : ''}`,
      timestamp: new Date().toISOString()
    }

    const newMessages = [...messages, userMessage]
    onSendMessage(newMessages)
    setUrlOptions({ show: false, url: '', processing: false })
    setInputMessage('')

    try {
      const response = await chatAPI.processUrl(url, question)
      
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.data.response,
        sources: [url],
        timestamp: new Date().toISOString(),
        isUrlResponse: true
      }

      onSendMessage([...newMessages, botMessage])
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: 'Error processing URL: ' + (error.response?.data?.error || error.message),
        timestamp: new Date().toISOString()
      }
      onSendMessage([...newMessages, errorMessage])
    }
  }

  const addUrlToKnowledge = async (url) => {
    setUrlOptions(prev => ({ ...prev, processing: true }))
    
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: `Adding URL to knowledge base: ${url}`,
      timestamp: new Date().toISOString()
    }

    const newMessages = [...messages, userMessage]
    onSendMessage(newMessages)
    setUrlOptions({ show: false, url: '', processing: false })
    setInputMessage('')

    try {
      const response = await chatAPI.addUrl(url)
      
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: `URL added successfully to knowledge base!\n\nFile created: ${response.data.filename}\nSummary: ${response.data.extraction_result?.summary || 'Not available'}`,
        timestamp: new Date().toISOString()
      }

      onSendMessage([...newMessages, botMessage])
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: 'Error adding URL: ' + (error.response?.data?.error || error.message),
        timestamp: new Date().toISOString()
      }
      onSendMessage([...newMessages, errorMessage])
    }
  }

  const askQuestionOnUrl = () => {
    const question = prompt('What question would you like to ask about this URL?')
    if (question) {
      processUrlImmediate(urlOptions.url, question)
    }
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="chat-header-left">
          <div className="chat-header-icon">
            <Sparkles size={20} color="#FF8A00" />
          </div>
          <div>
            <h2>AI Conversation</h2>
            <p className="chat-header-subtitle">Ask anything about your documents</p>
          </div>
        </div>
        <div className="chat-actions">
          <button onClick={onClearMessages} className="clear-btn">
            <Trash2 size={16} />
            Clear Chat
          </button>
        </div>
      </div>

      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">
              <Brain size={64} color="#FF8A00" />
            </div>
            <h3>Start a conversation</h3>
            <p>Ask a question about your documents or paste a URL to get started</p>
            <div className="empty-state-tips">
              <div className="tip">
                <Zap size={16} color="#FF8A00" />
                <span>Upload PDFs, images, or add website links</span>
              </div>
              <div className="tip">
                <Cpu size={16} color="#FF8A00" />
                <span>AI answers based only on your documents</span>
              </div>
            </div>
          </div>
        ) : (
          messages.map(message => (
            <div key={message.id} className={`message ${message.type}`}>
              <div className="message-avatar">
                {message.type === 'user' ? (
                  <User size={20} />
                ) : (
                  <img src={robotImage} alt="AI Assistant" className="robot-avatar" />
                )}
              </div>
              <div className="message-content">
                <div className="message-bubble">
                  {message.isUrlResponse && (
                    <div className="url-response-badge">
                      <Globe size={14} />
                      URL Response
                    </div>
                  )}
                  <div className="message-text">
                    {message.content}
                  </div>
                </div>
                {message.sources && message.sources.length > 0 && (
                  <div className="message-sources">
                    <div className="sources-label">Sources:</div>
                    <div className="sources-list">
                      {message.sources.map((source, index) => (
                        <span key={index} className="source-tag">
                          {source.startsWith('http') ? (
                            <a href={source} target="_blank" rel="noopener noreferrer" className="source-link">
                              <Link size={12} />
                              {new URL(source).hostname}
                            </a>
                          ) : (
                            source
                          )}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                <div className="message-time">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))
        )}
        
        {urlOptions.processing && (
          <div className="message bot">
            <div className="message-avatar">
              <img src={robotImage} alt="AI Assistant" className="robot-avatar" />
            </div>
            <div className="message-content">
              <div className="message-bubble">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <div className="url-processing-text">
                  <Globe size={16} />
                  Processing URL...
                </div>
              </div>
            </div>
          </div>
        )}

        {isLoading && !urlOptions.processing && (
          <div className="message bot">
            <div className="message-avatar">
              <img src={robotImage} alt="AI Assistant" className="robot-avatar" />
            </div>
            <div className="message-content">
              <div className="message-bubble">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <UrlModal 
        urlOptions={urlOptions}
        onClose={() => setUrlOptions({ show: false, url: '', processing: false })}
        onAnalyzeNow={() => processUrlImmediate(urlOptions.url)}
        onAddToKnowledge={() => addUrlToKnowledge(urlOptions.url)}
        onAskQuestion={askQuestionOnUrl}
      />

      <form onSubmit={handleSendMessage} className="message-input-form">
        <div className="input-group">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Ask a question or paste a URL..."
            disabled={isLoading || urlOptions.processing}
          />
          <button 
            type="submit" 
            disabled={isLoading || !inputMessage.trim() || urlOptions.processing}
          >
            {isLoading || urlOptions.processing ? <div className="loading-spinner"></div> : <Send size={20} />}
          </button>
        </div>
        <div className="input-hint">
          <Zap size={14} color="#FF8A00" />
          Paste a URL to analyze or add it to your knowledge base
        </div>
      </form>
    </div>
  )
}

export default Chat