import React, { useState } from 'react';
import axios from 'axios';
import './DiceRoller.css';

function DiceRoller({ campaignId }) {
  const [selectedDice, setSelectedDice] = useState('d20');
  const [count, setCount] = useState(1);
  const [modifier, setModifier] = useState(0);
  const [result, setResult] = useState(null);
  const [rolling, setRolling] = useState(false);

  const diceTypes = ['d4', 'd6', 'd8', 'd10', 'd12', 'd20', 'd100'];

  const rollDice = async () => {
    setRolling(true);
    try {
      const response = await axios.post(`/api/campaigns/${campaignId}/roll-dice`, {
        dice_type: selectedDice,
        count: count,
        modifier: modifier
      });

      setResult(response.data);
      
      setTimeout(() => {
        setRolling(false);
      }, 500);
    } catch (error) {
      console.error('Failed to roll dice:', error);
      setRolling(false);
    }
  };

  return (
    <div className="dice-roller">
      <h3>🎲 Dice Roller</h3>
      
      <div className="dice-selector">
        {diceTypes.map(dice => (
          <button
            key={dice}
            className={`dice-button ${selectedDice === dice ? 'active' : ''}`}
            onClick={() => setSelectedDice(dice)}
          >
            {dice}
          </button>
        ))}
      </div>

      <div className="dice-options">
        <div className="option-group">
          <label>Count</label>
          <input
            type="number"
            min="1"
            max="10"
            value={count}
            onChange={(e) => setCount(parseInt(e.target.value) || 1)}
          />
        </div>
        <div className="option-group">
          <label>Modifier</label>
          <input
            type="number"
            min="-10"
            max="10"
            value={modifier}
            onChange={(e) => setModifier(parseInt(e.target.value) || 0)}
          />
        </div>
      </div>

      <button 
        className="roll-button"
        onClick={rollDice}
        disabled={rolling}
      >
        {rolling ? '🎲 Rolling...' : `Roll ${count}${selectedDice}${modifier !== 0 ? (modifier > 0 ? `+${modifier}` : modifier) : ''}`}
      </button>

      {result && !rolling && (
        <div className="dice-result">
          <div className="result-header">Result</div>
          <div className="result-main">
            {result.final_total}
          </div>
          <div className="result-details">
            Rolls: [{result.rolls.join(', ')}]
            {result.modifier !== 0 && ` ${result.modifier > 0 ? '+' : ''}${result.modifier}`}
          </div>
        </div>
      )}
    </div>
  );
}

export default DiceRoller;
