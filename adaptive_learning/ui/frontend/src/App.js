import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react'
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

  const loadUserId = () => {
    let userId = localStorage.getItem('userId')
    if (!userId) {
      userId = 'user_' + Math.random().toString(36).substr(2, 9)
      localStorage.setItem('userId', userId)
    }
    return userId
  }

  const [messages, setMessages] = useState(loadMessages())
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [preferredFormat, setPreferredFormat] = useState(loadPreferredFormat())
  const [userId, setUserId] = useState(loadUserId())
  const [feedback, setFeedback] = useState('')
  const [feedbackRating, setFeedbackRating] = useState(0)
  const [feedbackRelevance, setFeedbackRelevance] = useState(0)
  const [feedbackEffectiveness, setFeedbackEffectiveness] = useState(0)
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false)
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
        body: JSON.stringify({ message: userMessage, format: preferredFormat, user_id: userId }),
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
    setMessages((prev) => [
      ...prev,
      {
        sender: 'bot',
        text: `Formato preferido alterado para: ${
          format === 'text' ? 'Texto' : format === 'video' ? 'Vídeo' : 'Áudio'
        }`,
        timestamp: new Date(),
        id: Date.now(),
      },
    ])
  }

  const handleFeedbackSubmit = useCallback(async () => {
    if (!feedback.trim()) return
    try {
      const response = await fetch('/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: `${feedback} (Avaliação Geral: ${feedbackRating}/5, Relevância do Conteúdo: ${feedbackRelevance}/5, Efetividade do Sistema: ${feedbackEffectiveness}/5)`,
          user_id: userId,
          format: preferredFormat,
        }),
      })
      const data = await response.json()
      if (data.status === 'success') {
        setFeedbackSubmitted(true)
        setFeedback('')
        setFeedbackRating(0)
        setFeedbackRelevance(0)
        setFeedbackEffectiveness(0)
        // Show a confirmation message for a short time
        setTimeout(() => setFeedbackSubmitted(false), 3000)
      }
    } catch (error) {
      console.error('Error submitting feedback:', error)
      setFeedbackSubmitted(true)
      setFeedback('')
      setFeedbackRating(0)
      setFeedbackRelevance(0)
      setFeedbackEffectiveness(0)
      setTimeout(() => setFeedbackSubmitted(false), 3000)
    }
  }, [feedback, feedbackRating, feedbackRelevance, feedbackEffectiveness, userId, preferredFormat])

  const handleClearChat = () => {
    if (window.confirm('Tem certeza de que deseja limpar o histórico de chat? Esta ação não pode ser desfeita.')) {
      setMessages([{ sender: 'bot', text: 'Olá! Como posso ajudar você hoje?', timestamp: new Date(), id: Date.now() }])
      localStorage.removeItem('chatMessages')
    }
  }

  const handleFeedbackKeyPress = useCallback(
    (e) => {
      if (e.key === 'Enter') {
        handleFeedbackSubmit()
      }
    },
    [handleFeedbackSubmit],
  )

  const formatTimestamp = (date) => {
    return new Intl.DateTimeFormat('pt-BR', {
      hour: '2-digit',
      minute: '2-digit',
    }).format(date)
  }

  // Memoize the message list to prevent unnecessary re-renders
  const messageList = useMemo(() => {
    return messages.map((msg) => (
      <div key={msg.id} className={`message ${msg.sender}`}>
        {msg.text}
        <span className="message-timestamp">{formatTimestamp(msg.timestamp)}</span>
      </div>
    ))
  }, [messages, formatTimestamp])

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>Sistema de Aprendizagem Adaptativa</h1>
      </div>
      <div className="chat-messages">
        {messageList}
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
            title="Receba conteúdo em formato de texto simples."
          >
            Texto
          </div>
          <div
            className={`pref-option ${preferredFormat === 'video' ? 'active' : ''}`}
            onClick={() => handleFormatChange('video')}
            title="Receba conteúdo em formato de vídeo explicativo."
          >
            Vídeo
          </div>
          <div
            className={`pref-option ${preferredFormat === 'audio' ? 'active' : ''}`}
            onClick={() => handleFormatChange('audio')}
            title="Receba conteúdo em formato de áudio para escutar."
          >
            Áudio
          </div>
        </div>
        <button onClick={handleClearChat} className="clear-chat-button">
          Limpar Chat
        </button>
        <div className="feedback-area">
          <input
            type="text"
            placeholder="Feedback sobre o conteúdo..."
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            onKeyPress={handleFeedbackKeyPress}
            className="feedback-input"
          />
          <div className="feedback-rating">
            <span>Avaliação Geral:</span>
            {[1, 2, 3, 4, 5].map((rating) => (
              <span
                key={rating}
                className={`rating-star ${feedbackRating >= rating ? 'active' : ''}`}
                onClick={() => setFeedbackRating(rating)}
              >
                ★
              </span>
            ))}
          </div>
          <div className="feedback-rating">
            <span>Relevância do Conteúdo:</span>
            {[1, 2, 3, 4, 5].map((rating) => (
              <span
                key={rating}
                className={`rating-star ${feedbackRelevance >= rating ? 'active' : ''}`}
                onClick={() => setFeedbackRelevance(rating)}
              >
                ★
              </span>
            ))}
          </div>
          <div className="feedback-rating">
            <span>Efetividade do Sistema:</span>
            {[1, 2, 3, 4, 5].map((rating) => (
              <span
                key={rating}
                className={`rating-star ${feedbackEffectiveness >= rating ? 'active' : ''}`}
                onClick={() => setFeedbackEffectiveness(rating)}
              >
                ★
              </span>
            ))}
          </div>
          <button onClick={handleFeedbackSubmit} className="feedback-button">
            Enviar Feedback
          </button>
          {feedbackSubmitted && <div className="feedback-confirmation">Obrigado pelo seu feedback!</div>}
        </div>
      </div>
    </div>
  )
}

export default App
