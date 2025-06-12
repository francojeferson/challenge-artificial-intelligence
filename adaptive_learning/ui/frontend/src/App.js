import React, { useState } from 'react'

function App() {
  const [messages, setMessages] = useState([{ sender: 'bot', text: 'Olá! Como posso ajudar você hoje?' }])
  const [input, setInput] = useState('')

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMessage = input.trim()
    setMessages((prev) => [...prev, { sender: 'user', text: userMessage }])
    setInput('')

    try {
      const response = await fetch('/api/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage }),
      })
      const data = await response.json()
      setMessages((prev) => [...prev, { sender: 'bot', text: data.response }])
    } catch (error) {
      setMessages((prev) => [...prev, { sender: 'bot', text: 'Erro ao se comunicar com o servidor.' }])
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage()
    }
  }

  return (
    <div style={{ maxWidth: 600, margin: '20px auto', fontFamily: 'Arial, sans-serif' }}>
      <h1>Sistema de Aprendizagem Adaptativa</h1>
      <div
        style={{
          border: '1px solid #ccc',
          padding: 10,
          height: 400,
          overflowY: 'auto',
          marginBottom: 10,
          backgroundColor: '#f9f9f9',
        }}
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              textAlign: msg.sender === 'user' ? 'right' : 'left',
              margin: '10px 0',
            }}
          >
            <span
              style={{
                display: 'inline-block',
                padding: '8px 12px',
                borderRadius: 15,
                backgroundColor: msg.sender === 'user' ? '#007bff' : '#e5e5ea',
                color: msg.sender === 'user' ? 'white' : 'black',
                maxWidth: '80%',
                wordWrap: 'break-word',
              }}
            >
              {msg.text}
            </span>
          </div>
        ))}
      </div>
      <input
        type="text"
        placeholder="Digite sua mensagem..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={handleKeyPress}
        style={{ width: '80%', padding: 10, fontSize: 16 }}
      />
      <button onClick={sendMessage} style={{ width: '18%', padding: 10, fontSize: 16, marginLeft: '2%' }}>
        Enviar
      </button>
    </div>
  )
}

export default App
