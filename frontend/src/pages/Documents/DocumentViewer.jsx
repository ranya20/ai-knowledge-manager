import React, { useState, useEffect } from 'react'
import { ArrowLeft, Download, FileText, X } from 'lucide-react'

const DocumentViewer = ({ document, module, onBack }) => {
  const [content, setContent] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadDocumentContent()
  }, [document])

  const loadDocumentContent = async () => {
    setLoading(true)
    try {
      // Simuler le chargement du contenu
      // Dans la réalité, vous feriez un appel API pour récupérer le contenu
      setTimeout(() => {
        setContent({
          text: `Contenu du document "${document.name}"\n\nCeci est un aperçu du document. Dans une implémentation réelle, vous récupéreriez le contenu depuis votre backend.\n\nTaille: ${document.size}\nDate: ${new Date(document.addedAt || document.uploadedAt).toLocaleString()}`
        })
        setLoading(false)
      }, 500)
    } catch (err) {
      setError("Impossible de charger le document")
      setLoading(false)
    }
  }

  const handleDownload = () => {
    // Logique de téléchargement
    alert(`Téléchargement de "${document.name}"`)
  }

  return (
    <div className="document-viewer">
      <div className="document-viewer-header">
        <button onClick={onBack} className="back-btn">
          <ArrowLeft size={20} />
          Retour au module
        </button>
        <div className="document-info">
          <FileText size={24} />
          <div>
            <h2>{document.name}</h2>
            <p>Module: {module.name}</p>
          </div>
        </div>
        <button onClick={handleDownload} className="download-btn">
          <Download size={20} />
          Télécharger
        </button>
      </div>

      <div className="document-viewer-content">
        {loading ? (
          <div className="loading-content">
            <div className="spinner"></div>
            <p>Chargement du document...</p>
          </div>
        ) : error ? (
          <div className="error-content">
            <X size={48} />
            <p>{error}</p>
          </div>
        ) : (
          <div className="document-text">
            <pre>{content?.text}</pre>
          </div>
        )}
      </div>
    </div>
  )
}

export default DocumentViewer