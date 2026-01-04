import React, { useEffect, useRef } from 'react';
import './ChatLog.css';

function ChatLog({ messages, characters }) {
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const getCharacterName = (characterId) => {
    const char = characters.find(c => c.id === characterId);
    return char ? char.name : 'Unknown';
  };

  const renderMessage = (msg) => {
    if (msg.role === 'dm') {
      return (
        <div key={msg.id} className="message dm-message">
          <div className="message-header">
            <span className="message-author dm-badge">🎲 Dungeon Master</span>
            <span className="message-time">
              {new Date(msg.timestamp).toLocaleTimeString()}
            </span>
          </div>
          <div className="message-content">{msg.content}</div>
        </div>
      );
    } else if (msg.role === 'player') {
      return (
        <div key={msg.id} className="message player-message">
          <div className="message-header">
            <span className="message-author player-badge">
              ⚔️ {getCharacterName(msg.character_id)}
            </span>
            <span className="message-time">
              {new Date(msg.timestamp).toLocaleTimeString()}
            </span>
          </div>
          <div className="message-content">{msg.content}</div>
        </div>
      );
    } else {
      return (
        <div key={msg.id} className="message system-message">
          <div className="message-content">{msg.content}</div>
        </div>
      );
    }
  };

  return (
    <div className="chat-log">
      <div className="chat-header">
        <h3>Adventure Log</h3>
      </div>
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="empty-state">
            <p>🎭 Your adventure begins...</p>
            <p className="empty-hint">
              Describe the opening scene to your AI party below
            </p>
          </div>
        ) : (
          messages.map(renderMessage)
        )}
        <div ref={chatEndRef} />
      </div>
    </div>
  );
}

export default ChatLog;
