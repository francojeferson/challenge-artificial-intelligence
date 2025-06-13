import React, { useState, useEffect, useRef } from 'react'
import './App.css'

function App() {
  // Load initial state from localStorage if available
  const loadMessages = () => {
    const savedMessages = localStorage.getItem('chatMessages')
    return savedMessages
      ? JSON.parse(savedMessages, (key, value) => {
          if (key === 'timestamp') {
            return new Date(value)
          }
          return value
        })
      : [{ sender: 'bot', text: 'Olá! Como posso ajudar você hoje?', timestamp: new Date(), id: Date.now() }]
  }

  const loadPreferredFormat = () => {
    return localStorage.getItem('preferredFormat') || 'text'
  }

  const [messages, setMessages] = useState(loadMessages())
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [preferredFormat, setPreferredFormat] = useState(loadPreferredFormat())
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Save messages and preferred format to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('chatMessages', JSON.stringify(messages))
  }, [messages])

  useEffect(() => {
    localStorage.setItem('preferredFormat', preferredFormat)
  }, [preferredFormat])

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMessage = input.trim()
    setMessages((prev) => [...prev, { sender: 'user', text: userMessage, timestamp: new Date(), id: Date.now() }])
    setInput('')
    setIsLoading(true)

    try {
      const response = await fetch('/api/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage, format: preferredFormat }),
      })
      const data = await response.json()
      // Check if the response contains a prompt and content separately
      let botText = data.response
      if (data.prompt && data.content && data.content.content) {
        botText = `${data.prompt}\n\n${data.content.content}`
      } else if (data.prompt) {
        botText = data.prompt
      }
      setMessages((prev) => [...prev, { sender: 'bot', text: botText, timestamp: new Date(), id: Date.now() }])
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: 'Erro ao se comunicar com o servidor.', timestamp: new Date(), id: Date.now() },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage()
    }
  }

  const handleFormatChange = (format) => {
    setPreferredFormat(format)
  }

  const formatTimestamp = (date) => {
    return new Intl.DateTimeFormat('pt-BR', {
      hour: '2-digit',
      minute: '2-digit',
    }).format(date)
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>Sistema de Aprendizagem Adaptativa</h1>
      </div>
      <div className="chat-messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.sender}`}>
            {msg.text}
            <span className="message-timestamp">{formatTimestamp(msg.timestamp)}</span>
          </div>
        ))}
        {isLoading && (
          <div className="loading-indicator">
            <div className="loading-dot"></div>
            <div className="loading-dot"></div>
            <div className="loading-dot"></div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input-area">
        <input
          type="text"
          placeholder="Digite sua mensagem..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          className="chat-input"
        />
        <button onClick={sendMessage} className="send-button">
          Enviar
        </button>
        <div className="preferences">
          <div
            className={`pref-option ${preferredFormat === 'text' ? 'active' : ''}`}
            onClick={() => handleFormatChange('text')}
          >
            Texto
          </div>
          <div
            className={`pref-option ${preferredFormat === 'video' ? 'active' : ''}`}
            onClick={() => handleFormatChange('video')}
          >
            Vídeo
          </div>
          <div
            className={`pref-option ${preferredFormat === 'audio' ? 'active' : ''}`}
            onClick={() => handleFormatChange('audio')}
          >
            Áudio
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
