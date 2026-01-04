import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './GameInterface.css';
import PartyView from './PartyView';
import ChatLog from './ChatLog';
import DMInterface from './DMInterface';
import DiceRoller from './DiceRoller';

function GameInterface({ campaignId, campaignData, onNewGame }) {
  const [characters, setCharacters] = useState([]);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCampaignData();
  }, [campaignId]);

  const loadCampaignData = async () => {
    try {
      const [charsResponse, msgsResponse] = await Promise.all([
        axios.get(`/api/campaigns/${campaignId}/characters`),
        axios.get(`/api/campaigns/${campaignId}/messages`)
      ]);

      setCharacters(charsResponse.data);
      setMessages(msgsResponse.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to load campaign data:', error);
      setLoading(false);
    }
  };

  const handleNewMessages = (newMessages) => {
    setMessages(prev => [...prev, ...newMessages]);
  };

  if (loading) {
    return <div className="loading">Loading campaign...</div>;
  }

  return (
    <div className="game-interface">
      <div className="game-header">
        <div className="campaign-info">
          <h2>{campaignData.name}</h2>
          <p>{campaignData.description}</p>
        </div>
        <button className="new-game-button" onClick={onNewGame}>
          New Campaign
        </button>
      </div>

      <div className="game-layout">
        <div className="left-panel">
          <PartyView characters={characters} />
          <DiceRoller campaignId={campaignId} />
        </div>

        <div className="main-panel">
          <ChatLog messages={messages} characters={characters} />
          <DMInterface 
            campaignId={campaignId} 
            characters={characters}
            onNewMessages={handleNewMessages}
          />
        </div>
      </div>
    </div>
  );
}

export default GameInterface;
