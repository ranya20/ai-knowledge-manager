import axios from 'axios'

const API_BASE = 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Intercepteur pour gérer les erreurs globales
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export const chatAPI = {
  ask: (question) => api.post('/ask', { question }),
  processUrl: (url, question) => api.post('/process-url', { url, question }),
  addUrl: (url) => api.post('/add-url', { url }),
}

export const documentsAPI = {
  upload: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  getFiles: () => api.get('/files'),
}

export const statsAPI = {
  getStats: () => api.get('/stats'),
}

export default api