from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models import Campaign, Character, Message, CombatState
from app.character_generator import CharacterGenerator
from app.ai_player import AIPlayer
from app.dice import DiceRoller
import asyncio
from concurrent.futures import ThreadPoolExecutor

class GameEngine:
    def __init__(self, db: Session):
        self.db = db
        self.ai_players: Dict[int, AIPlayer] = {}
        self.executor = ThreadPoolExecutor(max_workers=5)
    
    def create_campaign(self, name: str, description: str, party_size: int) -> Campaign:
        campaign = Campaign(
            name=name,
            description=description,
            party_size=party_size
        )
        self.db.add(campaign)
        self.db.commit()
        self.db.refresh(campaign)
        
        party = CharacterGenerator.generate_party(party_size)
        for char_data in party:
            character = Character(
                campaign_id=campaign.id,
                **char_data
            )
            self.db.add(character)
        
        combat_state = CombatState(campaign_id=campaign.id)
        self.db.add(combat_state)
        
        self.db.commit()
        
        self._initialize_ai_players(campaign.id)
        
        return campaign
    
    def _initialize_ai_players(self, campaign_id: int):
        characters = self.db.query(Character).filter(Character.campaign_id == campaign_id).all()
        for char in characters:
            char_dict = {
                "name": char.name,
                "race": char.race,
                "char_class": char.char_class,
                "level": char.level,
                "strength": char.strength,
                "dexterity": char.dexterity,
                "constitution": char.constitution,
                "intelligence": char.intelligence,
                "wisdom": char.wisdom,
                "charisma": char.charisma,
                "max_hp": char.max_hp,
                "current_hp": char.current_hp,
                "armor_class": char.armor_class,
                "personality_traits": char.personality_traits,
                "background": char.background,
                "inventory": char.inventory
            }
            self.ai_players[char.id] = AIPlayer(char_dict)
    
    def get_campaign(self, campaign_id: int) -> Optional[Campaign]:
        return self.db.query(Campaign).filter(Campaign.id == campaign_id).first()
    
    def get_characters(self, campaign_id: int) -> List[Character]:
        return self.db.query(Character).filter(Character.campaign_id == campaign_id).all()
    
    def add_message(self, campaign_id: int, role: str, content: str, 
                   character_id: Optional[int] = None, message_type: str = "narrative") -> Message:
        message = Message(
            campaign_id=campaign_id,
            character_id=character_id,
            role=role,
            content=content,
            message_type=message_type
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
    
    def get_messages(self, campaign_id: int, limit: int = 50) -> List[Message]:
        return self.db.query(Message)\
            .filter(Message.campaign_id == campaign_id)\
            .order_by(Message.timestamp.desc())\
            .limit(limit)\
            .all()
    
    async def get_party_responses(self, campaign_id: int, dm_message: str) -> List[Dict]:
        if campaign_id not in [player_id for player_id in self.ai_players.keys()]:
            self._initialize_ai_players(campaign_id)
        
        characters = self.get_characters(campaign_id)
        recent_messages = self.get_messages(campaign_id, limit=10)
        
        party_context = []
        for msg in reversed(recent_messages):
            role = "assistant" if msg.role == "player" else "user"
            party_context.append({"role": role, "content": msg.content})
        
        responses = []
        loop = asyncio.get_event_loop()
        
        for char in characters:
            if char.id in self.ai_players:
                response = await loop.run_in_executor(
                    self.executor,
                    self.ai_players[char.id].get_response,
                    dm_message,
                    party_context
                )
                
                responses.append({
                    "character_id": char.id,
                    "character_name": char.name,
                    "response": response
                })
                
                self.add_message(
                    campaign_id=campaign_id,
                    role="player",
                    content=f"{char.name}: {response}",
                    character_id=char.id
                )
        
        return responses
    
    def roll_dice(self, dice_type: str, count: int = 1, modifier: int = 0) -> Dict:
        dice_methods = {
            "d4": DiceRoller.d4,
            "d6": DiceRoller.d6,
            "d8": DiceRoller.d8,
            "d10": DiceRoller.d10,
            "d12": DiceRoller.d12,
            "d20": DiceRoller.d20,
            "d100": DiceRoller.d100
        }
        
        if dice_type not in dice_methods:
            return {"error": "Invalid dice type"}
        
        total, rolls = dice_methods[dice_type](count)
        final_total = total + modifier
        
        return {
            "dice_type": dice_type,
            "count": count,
            "rolls": rolls,
            "total": total,
            "modifier": modifier,
            "final_total": final_total
        }
    
    def start_combat(self, campaign_id: int) -> Dict:
        combat_state = self.db.query(CombatState).filter(CombatState.campaign_id == campaign_id).first()
        if not combat_state:
            return {"error": "Combat state not found"}
        
        characters = self.get_characters(campaign_id)
        initiative_order = []
        
        for char in characters:
            dex_mod = DiceRoller.modifier(char.dexterity)
            roll, _ = DiceRoller.d20()
            initiative = roll + dex_mod
            
            initiative_order.append({
                "character_id": char.id,
                "character_name": char.name,
                "initiative": initiative
            })
        
        initiative_order.sort(key=lambda x: x["initiative"], reverse=True)
        
        combat_state.is_active = True
        combat_state.current_turn = 0
        combat_state.round_number = 1
        combat_state.initiative_order = initiative_order
        self.db.commit()
        
        return {
            "message": "Combat started!",
            "initiative_order": initiative_order
        }
    
    def end_combat(self, campaign_id: int):
        combat_state = self.db.query(CombatState).filter(CombatState.campaign_id == campaign_id).first()
        if combat_state:
            combat_state.is_active = False
            combat_state.current_turn = 0
            combat_state.round_number = 1
            combat_state.initiative_order = []
            self.db.commit()
