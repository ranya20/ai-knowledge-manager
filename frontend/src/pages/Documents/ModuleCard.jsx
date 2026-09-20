import React, { useState } from 'react'
import { Folder, FileText, Edit, X, Check, Sparkles, Zap, MoreVertical, Trash2, BookOpen, Layers } from 'lucide-react'

const ModuleCard = ({ module, onClick, onDelete, onRename }) => {
  const [isEditing, setIsEditing] = useState(false)
  const [editName, setEditName] = useState(module.name)
  const [showMenu, setShowMenu] = useState(false)

  const handleRename = (e) => {
    e.stopPropagation()
    setIsEditing(true)
    setShowMenu(false)
  }

  const handleSave = (e) => {
    e.stopPropagation()
    if (editName.trim() && editName !== module.name) {
      onRename(editName)
    }
    setIsEditing(false)
  }

  const handleCancel = (e) => {
    e.stopPropagation()
    setEditName(module.name)
    setIsEditing(false)
  }

  const handleDelete = (e) => {
    e.stopPropagation()
    if (window.confirm(`Are you sure you want to delete module "${module.name}"? This action cannot be undone.`)) {
      onDelete()
    }
    setShowMenu(false)
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSave(e)
    } else if (e.key === 'Escape') {
      handleCancel(e)
    }
  }

  const fileCount = module.files?.length || 0
  const color = module.color || '#FF8A00'

  // Générer une couleur de fond basée sur la couleur du module
  const getGradientStyle = () => {
    return {
      background: `linear-gradient(135deg, ${color}20 0%, ${color}10 100%)`,
      borderTopColor: color
    }
  }

  return (
    <div className="module-card-premium" onClick={onClick}>
      <div className="module-card-premium-inner" style={getGradientStyle()}>
        {/* Header */}
        <div className="module-card-premium-header">
          <div className="module-icon-premium" style={{ background: `${color}20`, borderColor: `${color}40` }}>
            <Layers size={24} color={color} />
          </div>
          
          <div className="module-info-premium">
            {isEditing ? (
              <div className="module-edit-premium" onClick={(e) => e.stopPropagation()}>
                <input
                  type="text"
                  value={editName}
                  onChange={(e) => setEditName(e.target.value)}
                  onKeyDown={handleKeyPress}
                  autoFocus
                  className="module-edit-input"
                  placeholder="Module name"
                />
                <button onClick={handleSave} className="edit-action-btn save">
                  <Check size={14} />
                </button>
                <button onClick={handleCancel} className="edit-action-btn cancel">
                  <X size={14} />
                </button>
              </div>
            ) : (
              <>
                <h3 className="module-name-premium">{module.name}</h3>
                <div className="module-stats-premium">
                  <div className="stat-badge">
                    <FileText size={12} />
                    <span>{fileCount} {fileCount === 1 ? 'document' : 'documents'}</span>
                  </div>
                  {fileCount > 0 && (
                    <div className="stat-badge">
                      <Sparkles size={12} />
                      <span>AI Ready</span>
                    </div>
                  )}
                </div>
              </>
            )}
          </div>

          {!isEditing && (
            <div className="module-actions-premium">
              <button 
                onClick={(e) => {
                  e.stopPropagation()
                  setShowMenu(!showMenu)
                }} 
                className="menu-btn-premium"
                title="Module options"
              >
                <MoreVertical size={18} />
              </button>
              
              {showMenu && (
                <div className="module-dropdown-menu" onClick={(e) => e.stopPropagation()}>
                  <button onClick={handleRename} className="dropdown-item">
                    <Edit size={16} />
                    Rename
                  </button>
                  <button onClick={handleDelete} className="dropdown-item delete">
                    <Trash2 size={16} />
                    Delete
                  </button>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Preview / Stats Footer */}
        <div className="module-card-premium-footer">
          <div className="module-progress">
            <div className="progress-label">
              <Zap size={12} color="#FF8A00" />
              <span>Knowledge base</span>
            </div>
            <div className="progress-bar-container">
              <div 
                className="progress-bar-fill" 
                style={{ width: `${Math.min(fileCount * 10, 100)}%`, background: color }}
              />
            </div>
          </div>
          
          <div className="module-quick-actions">
            <button 
              onClick={(e) => {
                e.stopPropagation()
                onClick()
              }} 
              className="quick-action-btn"
            >
              <BookOpen size={14} />
              <span>Open</span>
            </button>
          </div>
        </div>

        {/* Decorative glow effect */}
        <div className="module-glow-premium" style={{ background: `radial-gradient(circle at 30% 30%, ${color}20 0%, transparent 70%)` }} />
      </div>
    </div>
  )
}

export default ModuleCard