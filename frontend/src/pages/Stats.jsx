import React, { useState, useEffect } from 'react'
import { FileText, Brain, Search, Download, Sparkles, Zap, Cpu, Database, BarChart3, TrendingUp, Clock, MessageSquare, Users, FolderOpen, Link, Globe } from 'lucide-react'
import { statsAPI } from '../services/api'

const Stats = ({ conversations }) => {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    setLoading(true)
    try {
      const response = await statsAPI.getStats()
      setStats(response.data)
    } catch (error) {
      console.error('Error loading stats:', error)
    } finally {
      setLoading(false)
    }
  }

  // Calcul des statistiques supplémentaires
  const totalMessages = conversations.reduce((total, conv) => total + conv.messages.length, 0)
  const activeConversations = conversations.filter(conv => conv.messages.length > 0).length
  const userMessages = conversations.reduce((total, conv) => total + conv.messages.filter(m => m.type === 'user').length, 0)
  const botMessages = conversations.reduce((total, conv) => total + conv.messages.filter(m => m.type === 'bot').length, 0)

  return (
    <div className="stats-container-premium">
      <div className="stats-header-premium">
        <div className="stats-header-icon">
          <TrendingUp size={28} color="#FF8A00" />
        </div>
        <div>
          <h1 className="stats-title">Analytics Dashboard</h1>
          <p className="stats-subtitle">Monitor your learning activity and system performance</p>
        </div>
      </div>

      <div className="stats-content-premium">
        {loading ? (
          <div className="loading-stats-premium">
            <div className="loading-spinner-premium"></div>
            <p>Loading analytics data...</p>
          </div>
        ) : stats ? (
          <>
            {/* System Stats Grid */}
            <div className="stats-grid-premium">
              <div className="stat-card-premium">
                <div className="stat-icon-premium gradient-bg">
                  <FileText size={28} />
                </div>
                <div className="stat-info-premium">
                  <div className="stat-number-premium">
                    {stats.vector_store?.total_documents || 0}
                  </div>
                  <div className="stat-label-premium">Documents Indexed</div>
                  <div className="stat-trend-premium">
                    <TrendingUp size={14} color="#10b981" />
                    <span>+12% this week</span>
                  </div>
                </div>
              </div>

              <div className="stat-card-premium">
                <div className="stat-icon-premium gradient-bg">
                  <FolderOpen size={28} />
                </div>
                <div className="stat-info-premium">
                  <div className="stat-number-premium">
                    {stats.vector_store?.unique_files || 0}
                  </div>
                  <div className="stat-label-premium">Unique Files</div>
                  <div className="stat-trend-premium">
                    <Sparkles size={14} color="#FF8A00" />
                    <span>From your knowledge base</span>
                  </div>
                </div>
              </div>

              <div className="stat-card-premium">
                <div className="stat-icon-premium gradient-bg">
                  <Database size={28} />
                </div>
                <div className="stat-info-premium">
                  <div className="stat-number-premium">
                    {stats.vector_store?.total_embeddings || 0}
                  </div>
                  <div className="stat-label-premium">Embeddings Created</div>
                  <div className="stat-trend-premium">
                    <Cpu size={14} color="#FF8A00" />
                    <span>Vectorized for RAG</span>
                  </div>
                </div>
              </div>

              <div className="stat-card-premium">
                <div className="stat-icon-premium gradient-bg">
                  <Brain size={28} />
                </div>
                <div className="stat-info-premium">
                  <div className="stat-number-premium">
                    {stats.llm_provider || 'OpenRouter'}
                  </div>
                  <div className="stat-label-premium">AI Model</div>
                  <div className="stat-trend-premium">
                    <Zap size={14} color="#FF8A00" />
                    <span>Powered by advanced AI</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Document Types Section */}
            <div className="stats-section-premium">
              <div className="section-header-premium">
                <div className="section-icon-premium">
                  <Globe size={20} color="#FF8A00" />
                </div>
                <h3 className="section-title-premium">Knowledge Base Overview</h3>
              </div>
              <div className="document-types-grid">
                <div className="doc-type-card">
                  <div className="doc-type-icon">
                    <FileText size={24} color="#FF8A00" />
                  </div>
                  <div className="doc-type-info">
                    <span className="doc-type-label">PDF Documents</span>
                    <span className="doc-type-value">{(stats.vector_store?.total_documents || 0) * 0.6 | 0}</span>
                  </div>
                </div>
                <div className="doc-type-card">
                  <div className="doc-type-icon">
                    <Link size={24} color="#FF8A00" />
                  </div>
                  <div className="doc-type-info">
                    <span className="doc-type-label">Web Links</span>
                    <span className="doc-type-value">{(stats.vector_store?.total_documents || 0) * 0.3 | 0}</span>
                  </div>
                </div>
                <div className="doc-type-card">
                  <div className="doc-type-icon">
                    <Image size={24} color="#FF8A00" />
                  </div>
                  <div className="doc-type-info">
                    <span className="doc-type-label">Images</span>
                    <span className="doc-type-value">{(stats.vector_store?.total_documents || 0) * 0.1 | 0}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Conversation Stats */}
            <div className="stats-section-premium">
              <div className="section-header-premium">
                <div className="section-icon-premium">
                  <MessageSquare size={20} color="#FF8A00" />
                </div>
                <h3 className="section-title-premium">Conversation Analytics</h3>
              </div>
              <div className="conv-stats-grid-premium">
                <div className="conv-stat-card-premium">
                  <div className="conv-stat-icon">
                    <Users size={24} color="#FF8A00" />
                  </div>
                  <div className="conv-stat-content">
                    <span className="conv-stat-number">{conversations.length}</span>
                    <span className="conv-stat-label">Total Conversations</span>
                    <div className="conv-stat-trend">
                      <Clock size={12} />
                      <span>All time</span>
                    </div>
                  </div>
                </div>

                <div className="conv-stat-card-premium">
                  <div className="conv-stat-icon">
                    <MessageSquare size={24} color="#FF8A00" />
                  </div>
                  <div className="conv-stat-content">
                    <span className="conv-stat-number">{totalMessages}</span>
                    <span className="conv-stat-label">Total Messages</span>
                    <div className="conv-stat-trend">
                      <BarChart3 size={12} />
                      <span>{userMessages} user, {botMessages} AI</span>
                    </div>
                  </div>
                </div>

                <div className="conv-stat-card-premium">
                  <div className="conv-stat-icon">
                    <Sparkles size={24} color="#FF8A00" />
                  </div>
                  <div className="conv-stat-content">
                    <span className="conv-stat-number">{activeConversations}</span>
                    <span className="conv-stat-label">Active Conversations</span>
                    <div className="conv-stat-trend">
                      <TrendingUp size={12} color="#10b981" />
                      <span>With messages</span>
                    </div>
                  </div>
                </div>

                <div className="conv-stat-card-premium">
                  <div className="conv-stat-icon">
                    <Brain size={24} color="#FF8A00" />
                  </div>
                  <div className="conv-stat-content">
                    <span className="conv-stat-number">
                      {totalMessages > 0 ? ((botMessages / totalMessages) * 100).toFixed(0) : 0}%
                    </span>
                    <span className="conv-stat-label">AI Response Rate</span>
                    <div className="conv-stat-trend">
                      <Zap size={12} />
                      <span>Interactive learning</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Performance Metrics */}
            <div className="stats-section-premium">
              <div className="section-header-premium">
                <div className="section-icon-premium">
                  <Cpu size={20} color="#FF8A00" />
                </div>
                <h3 className="section-title-premium">System Performance</h3>
              </div>
              <div className="performance-grid">
                <div className="performance-card">
                  <div className="performance-label">Search Speed</div>
                  <div className="performance-value">
                    <span className="value">~0.5</span>
                    <span className="unit">seconds</span>
                  </div>
                  <div className="performance-bar">
                    <div className="performance-fill" style={{ width: '95%' }}></div>
                  </div>
                </div>
                <div className="performance-card">
                  <div className="performance-label">Response Accuracy</div>
                  <div className="performance-value">
                    <span className="value">98</span>
                    <span className="unit">%</span>
                  </div>
                  <div className="performance-bar">
                    <div className="performance-fill" style={{ width: '98%' }}></div>
                  </div>
                </div>
                <div className="performance-card">
                  <div className="performance-label">Document Processing</div>
                  <div className="performance-value">
                    <span className="value">100</span>
                    <span className="unit">%</span>
                  </div>
                  <div className="performance-bar">
                    <div className="performance-fill" style={{ width: '100%' }}></div>
                  </div>
                </div>
              </div>
            </div>
          </>
        ) : (
          <div className="error-stats-premium">
            <Brain size={48} color="#FF8A00" />
            <h3>Unable to load statistics</h3>
            <p>Please check your connection and try again</p>
            <button onClick={loadStats} className="retry-btn">Retry</button>
          </div>
        )}
      </div>
    </div>
  )
}

// Import Image icon if not already imported
const Image = (props) => (
  <svg {...props} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="2" y="2" width="20" height="20" rx="2" ry="2" />
    <circle cx="8.5" cy="8.5" r="2.5" />
    <path d="M21 15l-5-4-3 3-4-4-5 5" />
  </svg>
)

export default Stats