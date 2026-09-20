import React, { useState, useEffect } from 'react'
import { Plus } from 'lucide-react'
import ModuleView from './ModuleView'
import DocumentViewer from './DocumentViewer'
import ModuleCard from './ModuleCard'
import { documentsAPI } from '../../services/api'

const Documents = () => {
  const [modules, setModules] = useState([])
  const [selectedModule, setSelectedModule] = useState(null)
  const [selectedDocument, setSelectedDocument] = useState(null)
  const [loading, setLoading] = useState(true)
  const [allProcessedFiles, setAllProcessedFiles] = useState([])

  useEffect(() => {
    loadModules()
    loadProcessedFiles()
  }, [])

  const loadModules = () => {
    const saved = localStorage.getItem('document-modules')
    if (saved) {
      setModules(JSON.parse(saved))
    } else {
      const defaultModules = [
        { id: 'module1', name: 'Module 1', files: [], color: '#FF8A00', createdAt: new Date().toISOString() },
        { id: 'module2', name: 'Module 2', files: [], color: '#FFA726', createdAt: new Date().toISOString() },
        { id: 'module3', name: 'Module 3', files: [], color: '#FF6F00', createdAt: new Date().toISOString() }
      ]
      setModules(defaultModules)
      saveModules(defaultModules)
    }
    setLoading(false)
  }

  const saveModules = (newModules) => {
    setModules(newModules)
    localStorage.setItem('document-modules', JSON.stringify(newModules))
  }

  const loadProcessedFiles = async () => {
    try {
      const response = await documentsAPI.getFiles()
      if (response.data && response.data.files) {
        setAllProcessedFiles(response.data.files)
      }
    } catch (error) {
      console.error('Error loading files:', error)
    }
  }

  const getRandomColor = () => {
    const colors = ['#FF8A00', '#FFA726', '#FF6F00', '#FF9800', '#FB8C00', '#F57C00']
    return colors[Math.floor(Math.random() * colors.length)]
  }

  const addNewModule = () => {
    const newModule = {
      id: 'module-' + Date.now(),
      name: `Module ${modules.length + 1}`,
      files: [],
      color: getRandomColor(),
      createdAt: new Date().toISOString()
    }
    saveModules([...modules, newModule])
  }

  const deleteModule = (moduleId) => {
    if (modules.length > 1) {
      saveModules(modules.filter(module => module.id !== moduleId))
    }
  }

  const updateModuleName = (moduleId, newName) => {
    saveModules(modules.map(module =>
      module.id === moduleId ? { ...module, name: newName } : module
    ))
  }

  const addFileToModule = (moduleId, file) => {
    let fileExists = false
    for (const module of modules) {
      if (module.id !== moduleId && module.files.some(f => f.name === file.name)) {
        fileExists = true
        break
      }
    }
    
    if (fileExists) {
      alert(`File "${file.name}" is already associated with another module.`)
      return false
    }
    
    const updatedModules = modules.map(module =>
      module.id === moduleId
        ? { ...module, files: [...module.files, { ...file, addedAt: new Date().toISOString() }] }
        : module
    )
    saveModules(updatedModules)
    loadProcessedFiles()
    return true
  }

  const removeFileFromModule = (moduleId, fileName) => {
    const updatedModules = modules.map(module =>
      module.id === moduleId
        ? { ...module, files: module.files.filter(f => f.name !== fileName) }
        : module
    )
    saveModules(updatedModules)
    loadProcessedFiles()
  }

  const handleModuleClick = (module) => {
    setSelectedModule(module)
    setSelectedDocument(null)
  }

  const handleBackToModules = () => {
    setSelectedModule(null)
    setSelectedDocument(null)
    loadProcessedFiles()
  }

  const handleDocumentClick = (document) => {
    setSelectedDocument(document)
  }

  const handleBackToModule = () => {
    setSelectedDocument(null)
  }

  if (selectedDocument && selectedModule) {
    return (
      <DocumentViewer
        document={selectedDocument}
        module={selectedModule}
        onBack={handleBackToModule}
      />
    )
  }

  if (selectedModule) {
    return (
      <ModuleView
        module={selectedModule}
        modules={modules}
        allProcessedFiles={allProcessedFiles}
        onBack={handleBackToModules}
        onDocumentClick={handleDocumentClick}
        onAddFile={addFileToModule}
        onRemoveFile={removeFileFromModule}
        onUpdateModule={updateModuleName}
        onDeleteModule={deleteModule}
        loadProcessedFiles={loadProcessedFiles}
      />
    )
  }

  return (
    <div className="documents-container">
      <div className="documents-header">
        <div>
          <h2>Documents</h2>
          <p>Organize your documents by modules</p>
        </div>
        <button onClick={addNewModule} className="add-module-btn">
          <Plus size={18} />
          New Module
        </button>
      </div>

      {loading ? (
        <div className="loading-modules">Loading modules...</div>
      ) : (
        <div className="modules-scroll-container">
          <div className="modules-grid">
            {modules.map(module => (
              <ModuleCard
                key={module.id}
                module={module}
                onClick={() => handleModuleClick(module)}
                onDelete={() => deleteModule(module.id)}
                onRename={(newName) => updateModuleName(module.id, newName)}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Documents