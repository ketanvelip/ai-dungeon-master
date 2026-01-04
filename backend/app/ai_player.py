from openai import OpenAI
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class AIPlayer:
    def __init__(self, character: Dict):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.character = character
        self.conversation_history = []
        
    def _build_system_prompt(self) -> str:
        personality_str = ", ".join(self.character["personality_traits"])
        
        return f"""You are {self.character['name']}, a {personality_str} {self.character['race']} {self.character['char_class']}.

CHARACTER STATS:
- Level: {self.character['level']}
- HP: {self.character['current_hp']}/{self.character['max_hp']}
- AC: {self.character['armor_class']}
- STR: {self.character['strength']}, DEX: {self.character['dexterity']}, CON: {self.character['constitution']}
- INT: {self.character['intelligence']}, WIS: {self.character['wisdom']}, CHA: {self.character['charisma']}

BACKGROUND: {self.character['background']}

EQUIPMENT: {', '.join(self.character['inventory'])}

ROLEPLAY INSTRUCTIONS:
- Stay in character at all times
- Your personality is {personality_str}
- Interact naturally with other party members
- Make decisions based on your character's traits and abilities
- You can discuss plans with other players before acting
- Be concise but expressive (2-4 sentences typically)
- Use first person ("I will..." not "My character will...")
- React to situations based on your personality
- Consider your abilities and equipment when making decisions

GAME MECHANICS:
- When you want to do something, describe your action clearly
- The DM will tell you when to roll dice
- In combat, state your intended action on your turn
- You can ask questions to the DM or other players
- Work together with your party members

Remember: You are a player in a D&D game, not the Dungeon Master. React to what the DM describes and make choices for your character."""

    def get_response(self, dm_message: str, party_context: Optional[List[Dict]] = None) -> str:
        messages = [{"role": "system", "content": self._build_system_prompt()}]
        
        if party_context:
            for msg in party_context[-10:]:
                messages.append(msg)
        
        messages.append({"role": "user", "content": dm_message})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.8,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[{self.character['name']} seems distracted and doesn't respond] (Error: {str(e)})"
    
    def get_combat_action(self, combat_situation: str, party_context: Optional[List[Dict]] = None) -> str:
        combat_prompt = f"""COMBAT SITUATION: {combat_situation}

It's your turn in combat. What do you do? 

Choose from:
- Attack (specify target and weapon)
- Cast Spell (if applicable)
- Use Item
- Move (specify where)
- Dodge
- Help another player
- Other creative action

State your action clearly and concisely."""

        return self.get_response(combat_prompt, party_context)
    
    def discuss_with_party(self, topic: str, other_responses: List[str]) -> str:
        discussion_context = f"""The party is discussing: {topic}

Other party members have said:
{chr(10).join(f"- {response}" for response in other_responses)}

What is your opinion or suggestion? Be brief."""

        return self.get_response(discussion_context)
    
    def update_character(self, updates: Dict):
        self.character.update(updates)
