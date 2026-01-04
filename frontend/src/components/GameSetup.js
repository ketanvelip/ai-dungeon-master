import React, { useState } from 'react';
import axios from 'axios';
import './GameSetup.css';

function GameSetup({ onCampaignCreated }) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [partySize, setPartySize] = useState(3);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/api/campaigns', {
        name: name || 'Untitled Campaign',
        description: description || 'A new adventure begins...',
        party_size: partySize
      });

      onCampaignCreated(response.data.id, response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create campaign');
      setLoading(false);
    }
  };

  return (
    <div className="game-setup">
      <div className="setup-card">
        <h2>Create Your Campaign</h2>
        <p className="setup-description">
          Set up your adventure and let AI generate your party of adventurers
        </p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Campaign Name</label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="The Lost Mines of Phandelver"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Description (Optional)</label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="A tale of heroes seeking fortune and glory..."
              rows="3"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="partySize">Party Size</label>
            <div className="party-size-selector">
              {[1, 2, 3, 4, 5, 6].map(size => (
                <button
                  key={size}
                  type="button"
                  className={`size-button ${partySize === size ? 'active' : ''}`}
                  onClick={() => setPartySize(size)}
                  disabled={loading}
                >
                  {size}
                </button>
              ))}
            </div>
            <small>Recommended: 3-4 characters</small>
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="create-button" disabled={loading}>
            {loading ? 'Creating Party...' : 'Create Campaign'}
          </button>
        </form>

        <div className="setup-info">
          <h3>How It Works</h3>
          <ul>
            <li>🎭 AI generates unique characters with distinct personalities</li>
            <li>💬 Characters interact with each other naturally</li>
            <li>🎲 Full D&D mechanics with dice rolling and combat</li>
            <li>🤖 Get AI suggestions to enhance your storytelling</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default GameSetup;
