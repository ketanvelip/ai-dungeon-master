from openai import OpenAI
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

# Model configuration
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

class DMAssistant:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = DEFAULT_MODEL
    
    def suggest_scenarios(self, context: str, party_info: List[Dict]) -> List[str]:
        party_summary = self._summarize_party(party_info)
        
        prompt = f"""You are assisting a Dungeon Master in a D&D game.

PARTY COMPOSITION:
{party_summary}

CURRENT CONTEXT:
{context if context else "Starting a new adventure"}

Generate 3 diverse scenario suggestions for the DM. Each should be:
- Engaging and appropriate for the party level
- Different in tone (combat, social, exploration, mystery, etc.)
- Brief (1-2 sentences each)
- Actionable

Format as a numbered list."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a creative D&D scenario generator helping a DM."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=300
            )
            
            suggestions_text = response.choices[0].message.content.strip()
            suggestions = [line.strip() for line in suggestions_text.split('\n') if line.strip() and any(c.isdigit() for c in line[:3])]
            
            return suggestions[:3] if suggestions else [
                "1. A mysterious stranger approaches with a quest",
                "2. Strange sounds echo from a nearby cave",
                "3. The party encounters bandits on the road"
            ]
        except Exception as e:
            return [
                "1. A mysterious stranger approaches with a quest",
                "2. Strange sounds echo from a nearby cave",
                "3. The party encounters bandits on the road"
            ]
    
    def suggest_npc_dialogue(self, npc_description: str, situation: str) -> str:
        prompt = f"""Generate a brief dialogue line for an NPC in a D&D game.

NPC: {npc_description}
SITUATION: {situation}

Provide a single line of dialogue (1-2 sentences) that this NPC would say. Make it flavorful and in-character."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a D&D NPC dialogue generator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=100
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return "[NPC speaks but you can't quite make out the words]"
    
    def suggest_encounter(self, party_level: int, environment: str) -> Dict:
        prompt = f"""Generate a combat encounter for a D&D party.

Party Level: {party_level}
Environment: {environment}

Provide:
1. Enemy type(s) and number
2. Brief tactical setup
3. Potential complications

Keep it brief and balanced for the party level."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a D&D encounter designer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=200
            )
            
            return {
                "description": response.choices[0].message.content.strip(),
                "difficulty": "medium"
            }
        except Exception as e:
            return {
                "description": f"A group of enemies appears in the {environment}",
                "difficulty": "medium"
            }
    
    def _summarize_party(self, party_info: List[Dict]) -> str:
        summary = []
        for char in party_info:
            personality = ", ".join(char.get("personality_traits", []))
            summary.append(f"- {char['name']}: Level {char['level']} {char['race']} {char['char_class']} ({personality})")
        return "\n".join(summary)
