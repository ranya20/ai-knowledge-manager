import React, { useState, useEffect } from 'react'
import { ArrowLeft, Upload, FileText, X, Plus, Trash2, Eye, RefreshCw, Sparkles, Zap, CheckCircle, AlertCircle, Clock, HardDrive, BookOpen, Layers } from 'lucide-react'
import { documentsAPI } from '../../services/api'

const ModuleView = ({ 
  module, 
  modules, 
  allProcessedFiles,
  onBack, 
  onDocumentClick, 
  onAddFile, 
  onRemoveFile,
  onUpdateModule,
  onDeleteModule,
  loadProcessedFiles 
}) => {
  const [uploadedFiles, setUploadedFiles] = useState([])
  const [isUploading, setIsUploading] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [editName, setEditName] = useState(module.name)
  const [availableFiles, setAvailableFiles] = useState([])

  useEffect(() => {
    updateAvailableFiles()
  }, [allProcessedFiles, module.files, modules])

  const updateAvailableFiles = () => {
    const moduleFileNames = module.files?.map(f => f.name) || []
    const allModuleFiles = modules.flatMap(m => m.files?.map(f => f.name) || [])
    const available = allProcessedFiles.filter(f => 
      !moduleFileNames.includes(f.name) && !allModuleFiles.includes(f.name)
    )
    setAvailableFiles(available)
  }

  const handleUpload = async (e) => {
    const files = Array.from(e.target.files)
    if (files.length === 0) return

    setIsUploading(true)
    
    for (const file of files) {
      const tempFile = {
        name: file.name,
        size: (file.size / 1024 / 1024).toFixed(2) + ' MB',
        status: 'uploading'
      }
      setUploadedFiles(prev => [...prev, tempFile])

      try {
        const response = await documentsAPI.upload(file)
        
        setUploadedFiles(prev => 
          prev.map(f => f.name === file.name ? { ...f, status: 'success' } : f)
        )
        
        onAddFile(module.id, {
          name: file.name,
          size: (file.size / 1024 / 1024).toFixed(2) + ' MB',
          uploadedAt: new Date().toISOString(),
          content: response.data
        })
        
        await loadProcessedFiles()
        updateAvailableFiles()
        
      } catch (error) {
        console.error('Upload error:', error)
        setUploadedFiles(prev => 
          prev.map(f => f.name === file.name ? { ...f, status: 'error', error: 'Upload failed' } : f)
        )
      }
    }
    
    setTimeout(() => {
      setUploadedFiles([])
      setIsUploading(false)
    }, 2000)
  }

  const handleAddExistingFile = async (file) => {
    let fileInOtherModule = false
    for (const mod of modules) {
      if (mod.id !== module.id && mod.files.some(f => f.name === file.name)) {
        fileInOtherModule = true
        break
      }
    }
    
    if (fileInOtherModule) {
      alert(`File "${file.name}" is already associated with another module.`)
      return
    }
    
    const success = onAddFile(module.id, {
      name: file.name,
      size: file.size,
      addedAt: new Date().toISOString()
    })
    
    if (success !== false) {
      updateAvailableFiles()
    }
  }

  const handleRemoveFile = (fileName) => {
    if (window.confirm(`Remove "${fileName}" from this module?`)) {
      onRemoveFile(module.id, fileName)
      updateAvailableFiles()
    }
  }

  const handleRenameModule = () => {
    if (editName.trim() && editName !== module.name) {
      onUpdateModule(module.id, editName)
      setIsEditing(false)
    }
  }

  const handleDeleteModule = () => {
    if (window.confirm(`Are you sure you want to permanently delete module "${module.name}"? This action cannot be undone.`)) {
      onDeleteModule(module.id)
      onBack()
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleRenameModule()
    } else if (e.key === 'Escape') {
      setIsEditing(false)
      setEditName(module.name)
    }
  }

  const formatDate = (date) => {
    if (!date) return 'Unknown date'
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  const getStatusIcon = (status) => {
    switch(status) {
      case 'success': return <CheckCircle size={14} color="#10b981" />
      case 'error': return <AlertCircle size={14} color="#ef4444" />
      default: return <Clock size={14} color="#FF8A00" />
    }
  }

  return (
    <div className="module-view-premium">
      {/* Header */}
      <div className="module-view-header-premium">
        <div className="header-top">
          <button onClick={onBack} className="back-btn-premium">
            <ArrowLeft size={18} />
            Back to Modules
          </button>
          <div className="header-actions">
            <button onClick={updateAvailableFiles} className="refresh-btn-premium" title="Refresh">
              <RefreshCw size={18} />
            </button>
          </div>
        </div>
        
        <div className="module-title-section">
          <div className="module-icon-large">
            <Layers size={32} color="#FF8A00" />
          </div>
          <div className="module-title-content">
            {isEditing ? (
              <div className="module-edit-inline-premium">
                <input
                  type="text"
                  value={editName}
                  onChange={(e) => setEditName(e.target.value)}
                  onKeyDown={handleKeyPress}
                  autoFocus
                  className="module-edit-input-premium"
                  placeholder="Module name"
                />
                <button onClick={handleRenameModule} className="save-btn-premium">
                  Save
                </button>
                <button onClick={() => {
                  setIsEditing(false)
                  setEditName(module.name)
                }} className="cancel-btn-premium">
                  Cancel
                </button>
              </div>
            ) : (
              <>
                <h1 className="module-title-premium">{module.name}</h1>
                <div className="module-badges">
                  <div className="module-badge">
                    <FileText size={14} />
                    <span>{module.files?.length || 0} documents</span>
                  </div>
                  <div className="module-badge">
                    <Sparkles size={14} />
                    <span>AI Ready</span>
                  </div>
                  <button onClick={() => setIsEditing(true)} className="edit-name-btn">
                    <Edit size={14} />
                    Rename
                  </button>
                  <button onClick={handleDeleteModule} className="delete-module-btn-premium">
                    <Trash2 size={14} />
                    Delete
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Content Area with Scroll */}
      <div className="module-view-content-premium">
        {/* Upload Section */}
        <div className="upload-section-premium">
          <div className="section-header">
            <div className="section-icon">
              <Upload size={18} color="#FF8A00" />
            </div>
            <h3>Add Documents</h3>
          </div>
          <div className="upload-buttons">
            <label className="upload-btn-premium">
              <Upload size={18} />
              Upload New Files
              <input
                type="file"
                multiple
                onChange={handleUpload}
                accept=".pdf,.txt,.jpg,.jpeg,.png,.docx,.md"
                style={{ display: 'none' }}
              />
            </label>
          </div>

          {/* Upload Status */}
          {uploadedFiles.length > 0 && (
            <div className="upload-status-premium">
              {uploadedFiles.map((file, index) => (
                <div key={index} className={`upload-item-premium ${file.status}`}>
                  {getStatusIcon(file.status)}
                  <span className="file-name">{file.name}</span>
                  <span className="status-text">
                    {file.status === 'uploading' && 'Uploading...'}
                    {file.status === 'success' && 'Completed'}
                    {file.status === 'error' && file.error}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Available Files Section */}
        {availableFiles.length > 0 && (
          <div className="available-files-premium">
            <div className="section-header">
              <div className="section-icon">
                <HardDrive size={18} color="#FF8A00" />
              </div>
              <h3>Available Processed Files ({availableFiles.length})</h3>
            </div>
            <div className="available-files-grid">
              {availableFiles.map((file, index) => (
                <div key={index} className="available-file-card">
                  <div className="file-icon">
                    <FileText size={20} color="#FF8A00" />
                  </div>
                  <div className="file-info">
                    <div className="file-name">{file.name}</div>
                    <div className="file-meta">{file.size}</div>
                  </div>
                  <button 
                    onClick={() => handleAddExistingFile(file)} 
                    className="add-file-btn-premium"
                    title="Add to module"
                  >
                    <Plus size={16} />
                    Add
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Module Files Section */}
        <div className="module-files-premium">
          <div className="section-header">
            <div className="section-icon">
              <BookOpen size={18} color="#FF8A00" />
            </div>
            <h3>Documents in this module ({module.files?.length || 0})</h3>
          </div>
          
          {module.files && module.files.length > 0 ? (
            <div className="files-grid-premium">
              {module.files.map((file, index) => (
                <div key={index} className="file-card-premium">
                  <div className="file-card-icon-premium">
                    <FileText size={28} color="#FF8A00" />
                  </div>
                  <div className="file-card-info-premium">
                    <div className="file-name-premium" title={file.name}>
                      {file.name}
                    </div>
                    <div className="file-meta-premium">
                      <span className="file-size">{file.size}</span>
                      <span className="file-date">Added {formatDate(file.addedAt || file.uploadedAt)}</span>
                    </div>
                  </div>
                  <div className="file-card-actions-premium">
                    <button 
                      onClick={() => onDocumentClick(file)} 
                      className="view-file-btn"
                      title="View document"
                    >
                      <Eye size={18} />
                    </button>
                    <button 
                      onClick={() => handleRemoveFile(file.name)} 
                      className="remove-file-btn"
                      title="Remove from module"
                    >
                      <Trash2 size={18} />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-module-premium">
              <div className="empty-icon">
                <FileText size={64} color="#FF8A00" opacity={0.5} />
              </div>
              <h4>No documents yet</h4>
              <p>Upload files or add from available processed files to get started</p>
              <div className="empty-tips">
                <div className="tip">
                  <Zap size={14} color="#FF8A00" />
                  <span>PDF, images, and text files supported</span>
                </div>
                <div className="tip">
                  <Sparkles size={14} color="#FF8A00" />
                  <span>AI will analyze and index your documents</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// Import Edit icon
const Edit = (props) => (
  <svg {...props} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M17 3l4 4-7 7H10v-4l7-7z" />
    <path d="M4 20h16" />
  </svg>
)

export default ModuleView