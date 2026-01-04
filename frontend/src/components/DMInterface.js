import React, { useState } from 'react';
import axios from 'axios';
import './DMInterface.css';

function DMInterface({ campaignId, characters, onNewMessages }) {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [loadingSuggestions, setLoadingSuggestions] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim() || loading) return;

    setLoading(true);
    const dmMessage = message;
    setMessage('');

    try {
      const response = await axios.post(`/api/campaigns/${campaignId}/dm-input`, {
        message: dmMessage
      });

      const newMessages = [
        {
          id: Date.now(),
          role: 'dm',
          content: dmMessage,
          timestamp: new Date().toISOString()
        },
        ...response.data.party_responses.map((resp, idx) => ({
          id: Date.now() + idx + 1,
          role: 'player',
          content: resp.response,
          character_id: resp.character_id,
          timestamp: new Date().toISOString()
        }))
      ];

      onNewMessages(newMessages);
    } catch (error) {
      console.error('Failed to send message:', error);
      alert('Failed to get party response. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getSuggestions = async () => {
    setLoadingSuggestions(true);
    try {
      const response = await axios.post(`/api/dm-assistant/scenarios`, {
        context: message || ''
      }, {
        params: { campaign_id: campaignId }
      });

      setSuggestions(response.data.suggestions);
      setShowSuggestions(true);
    } catch (error) {
      console.error('Failed to get suggestions:', error);
      alert('Failed to get suggestions. Please try again.');
    } finally {
      setLoadingSuggestions(false);
    }
  };

  const applySuggestion = (suggestion) => {
    const cleanSuggestion = suggestion.replace(/^\d+\.\s*/, '');
    setMessage(cleanSuggestion);
    setShowSuggestions(false);
  };

  return (
    <div className="dm-interface">
      <div className="dm-header">
        <h3>Dungeon Master Controls</h3>
        <button 
          className="suggestion-button"
          onClick={getSuggestions}
          disabled={loadingSuggestions}
        >
          {loadingSuggestions ? '🤔 Thinking...' : '💡 Get Suggestions'}
        </button>
      </div>

      {showSuggestions && suggestions.length > 0 && (
        <div className="suggestions-panel">
          <div className="suggestions-header">
            <h4>AI Suggestions</h4>
            <button 
              className="close-suggestions"
              onClick={() => setShowSuggestions(false)}
            >
              ✕
            </button>
          </div>
          <div className="suggestions-list">
            {suggestions.map((suggestion, idx) => (
              <div 
                key={idx} 
                className="suggestion-item"
                onClick={() => applySuggestion(suggestion)}
              >
                {suggestion}
              </div>
            ))}
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="dm-form">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Describe what happens next... (e.g., 'You enter a dark tavern. A hooded figure watches from the corner.')"
          rows="4"
          disabled={loading}
        />
        <div className="dm-actions">
          <div className="character-count">
            {message.length} characters
          </div>
          <button 
            type="submit" 
            className="send-button"
            disabled={!message.trim() || loading}
          >
            {loading ? '⏳ Waiting for party...' : '📜 Narrate to Party'}
          </button>
        </div>
      </form>

      <div className="dm-tips">
        <strong>DM Tips:</strong>
        <ul>
          <li>Describe scenes vividly to engage your AI players</li>
          <li>Ask questions to prompt specific responses</li>
          <li>Present choices or challenges for the party to discuss</li>
          <li>Use the dice roller for skill checks and combat</li>
        </ul>
      </div>
    </div>
  );
}

export default DMInterface;
