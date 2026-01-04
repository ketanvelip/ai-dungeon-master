import React, { useState } from 'react';
import './App.css';
import GameSetup from './components/GameSetup';
import GameInterface from './components/GameInterface';

function App() {
  const [campaignId, setCampaignId] = useState(null);
  const [campaignData, setCampaignData] = useState(null);

  const handleCampaignCreated = (id, data) => {
    setCampaignId(id);
    setCampaignData(data);
  };

  const handleNewGame = () => {
    setCampaignId(null);
    setCampaignData(null);
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🎲 AI Dungeon Master</h1>
        <p>You are the DM. AI players bring your story to life.</p>
      </header>

      <div className="game-container">
        {!campaignId ? (
          <GameSetup onCampaignCreated={handleCampaignCreated} />
        ) : (
          <GameInterface 
            campaignId={campaignId} 
            campaignData={campaignData}
            onNewGame={handleNewGame}
          />
        )}
      </div>
    </div>
  );
}

export default App;
