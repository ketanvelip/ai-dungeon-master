import React from 'react';
import './PartyView.css';

function PartyView({ characters }) {
  const getModifier = (score) => {
    const mod = Math.floor((score - 10) / 2);
    return mod >= 0 ? `+${mod}` : `${mod}`;
  };

  return (
    <div className="party-view">
      <h3>Your Party</h3>
      <div className="characters-list">
        {characters.map(char => (
          <div key={char.id} className="character-card">
            <div className="character-header">
              <h4>{char.name}</h4>
              <span className="character-level">Lvl {char.level}</span>
            </div>
            
            <div className="character-class">
              {char.race} {char.char_class}
            </div>
            
            <div className="character-hp">
              <div className="hp-bar">
                <div 
                  className="hp-fill" 
                  style={{width: `${(char.current_hp / char.max_hp) * 100}%`}}
                />
              </div>
              <span className="hp-text">
                {char.current_hp}/{char.max_hp} HP
              </span>
            </div>
            
            <div className="character-stats">
              <div className="stat">
                <span className="stat-label">AC</span>
                <span className="stat-value">{char.armor_class}</span>
              </div>
              <div className="stat">
                <span className="stat-label">STR</span>
                <span className="stat-value">{getModifier(char.strength)}</span>
              </div>
              <div className="stat">
                <span className="stat-label">DEX</span>
                <span className="stat-value">{getModifier(char.dexterity)}</span>
              </div>
              <div className="stat">
                <span className="stat-label">CON</span>
                <span className="stat-value">{getModifier(char.constitution)}</span>
              </div>
              <div className="stat">
                <span className="stat-label">INT</span>
                <span className="stat-value">{getModifier(char.intelligence)}</span>
              </div>
              <div className="stat">
                <span className="stat-label">WIS</span>
                <span className="stat-value">{getModifier(char.wisdom)}</span>
              </div>
              <div className="stat">
                <span className="stat-label">CHA</span>
                <span className="stat-value">{getModifier(char.charisma)}</span>
              </div>
            </div>
            
            <div className="character-personality">
              {char.personality_traits.map((trait, idx) => (
                <span key={idx} className="trait-badge">{trait}</span>
              ))}
            </div>
            
            <details className="character-details">
              <summary>Background & Items</summary>
              <p className="background-text">{char.background}</p>
              <div className="inventory">
                <strong>Inventory:</strong>
                <ul>
                  {char.inventory.map((item, idx) => (
                    <li key={idx}>{item}</li>
                  ))}
                </ul>
              </div>
            </details>
          </div>
        ))}
      </div>
    </div>
  );
}

export default PartyView;
