import { useState, useEffect } from 'react'

export const useConversations = () => {
  const [conversations, setConversations] = useState([])
  const [currentConversation, setCurrentConversation] = useState(null)
  const [messages, setMessages] = useState([])

  // Charger les conversations depuis localStorage
  useEffect(() => {
    const saved = localStorage.getItem('rag-conversations')
    if (saved) {
      const conversationsData = JSON.parse(saved)
      setConversations(conversationsData)
      if (conversationsData.length > 0) {
        setCurrentConversation(conversationsData[0].id)
        setMessages(conversationsData[0].messages)
      }
    } else {
      const defaultConv = {
        id: 'default',
        title: 'Nouvelle conversation',
        messages: [],
        createdAt: new Date().toISOString()
      }
      setConversations([defaultConv])
      setCurrentConversation('default')
    }
  }, [])

  // Sauvegarder les conversations
  const saveConversations = (newConversations) => {
    setConversations(newConversations)
    localStorage.setItem('rag-conversations', JSON.stringify(newConversations))
  }

  // Sauvegarder les messages de la conversation courante
  const saveMessages = (newMessages) => {
    setMessages(newMessages)
    const updatedConversations = conversations.map(conv =>
      conv.id === currentConversation
        ? {
            ...conv,
            messages: newMessages,
            title: newMessages[0]?.content?.substring(0, 30) + '...' || 'Nouvelle conversation'
          }
        : conv
    )
    saveConversations(updatedConversations)
  }

  // Nouvelle conversation
  const newConversation = () => {
    const newConv = {
      id: 'conv-' + Date.now(),
      title: 'Nouvelle conversation',
      messages: [],
      createdAt: new Date().toISOString()
    }
    const updated = [newConv, ...conversations]
    saveConversations(updated)
    setCurrentConversation(newConv.id)
    setMessages([])
    return newConv.id
  }

  // Changer de conversation
  const switchConversation = (convId) => {
    const conversation = conversations.find(c => c.id === convId)
    if (conversation) {
      setCurrentConversation(convId)
      setMessages(conversation.messages)
    }
  }

  // Supprimer une conversation
  const deleteConversation = (convId) => {
    const updated = conversations.filter(c => c.id !== convId)
    saveConversations(updated)
    
    if (currentConversation === convId) {
      if (updated.length > 0) {
        setCurrentConversation(updated[0].id)
        setMessages(updated[0].messages)
      } else {
        newConversation()
      }
    }
  }

  // Effacer les messages de la conversation courante
  const clearMessages = () => {
    saveMessages([])
  }

  return {
    conversations,
    currentConversation,
    messages,
    saveMessages,
    newConversation,
    switchConversation,
    deleteConversation,
    clearMessages,
  }
}