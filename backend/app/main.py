from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.database import get_db, init_db
from app.game_engine import GameEngine
from app.dm_assistant import DMAssistant
from app.models import Campaign, Character, Message
import asyncio

app = FastAPI(title="AI Dungeon Master API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

class CampaignCreate(BaseModel):
    name: str
    description: str
    party_size: int

class DMInput(BaseModel):
    message: str

class DiceRoll(BaseModel):
    dice_type: str
    count: int = 1
    modifier: int = 0

class ScenarioRequest(BaseModel):
    context: str = ""

@app.get("/")
def read_root():
    return {"message": "AI Dungeon Master API", "status": "running"}

@app.post("/campaigns")
def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    if campaign.party_size < 1 or campaign.party_size > 6:
        raise HTTPException(status_code=400, detail="Party size must be between 1 and 6")
    
    engine = GameEngine(db)
    new_campaign = engine.create_campaign(
        name=campaign.name,
        description=campaign.description,
        party_size=campaign.party_size
    )
    
    return {
        "id": new_campaign.id,
        "name": new_campaign.name,
        "description": new_campaign.description,
        "party_size": new_campaign.party_size,
        "created_at": new_campaign.created_at
    }

@app.get("/campaigns/{campaign_id}")
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    engine = GameEngine(db)
    campaign = engine.get_campaign(campaign_id)
    
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    return {
        "id": campaign.id,
        "name": campaign.name,
        "description": campaign.description,
        "party_size": campaign.party_size,
        "created_at": campaign.created_at,
        "is_active": campaign.is_active
    }

@app.get("/campaigns/{campaign_id}/characters")
def get_characters(campaign_id: int, db: Session = Depends(get_db)):
    engine = GameEngine(db)
    characters = engine.get_characters(campaign_id)
    
    return [
        {
            "id": char.id,
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
        for char in characters
    ]

@app.post("/campaigns/{campaign_id}/dm-input")
async def dm_input(campaign_id: int, dm_input: DMInput, db: Session = Depends(get_db)):
    engine = GameEngine(db)
    campaign = engine.get_campaign(campaign_id)
    
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    engine.add_message(
        campaign_id=campaign_id,
        role="dm",
        content=dm_input.message,
        message_type="narrative"
    )
    
    responses = await engine.get_party_responses(campaign_id, dm_input.message)
    
    return {
        "dm_message": dm_input.message,
        "party_responses": responses
    }

@app.get("/campaigns/{campaign_id}/messages")
def get_messages(campaign_id: int, limit: int = 50, db: Session = Depends(get_db)):
    engine = GameEngine(db)
    messages = engine.get_messages(campaign_id, limit)
    
    return [
        {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "character_id": msg.character_id,
            "message_type": msg.message_type,
            "timestamp": msg.timestamp
        }
        for msg in reversed(messages)
    ]

@app.post("/campaigns/{campaign_id}/roll-dice")
def roll_dice(campaign_id: int, dice_roll: DiceRoll, db: Session = Depends(get_db)):
    engine = GameEngine(db)
    result = engine.roll_dice(
        dice_type=dice_roll.dice_type,
        count=dice_roll.count,
        modifier=dice_roll.modifier
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@app.post("/campaigns/{campaign_id}/combat/start")
def start_combat(campaign_id: int, db: Session = Depends(get_db)):
    engine = GameEngine(db)
    result = engine.start_combat(campaign_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@app.post("/campaigns/{campaign_id}/combat/end")
def end_combat(campaign_id: int, db: Session = Depends(get_db)):
    engine = GameEngine(db)
    engine.end_combat(campaign_id)
    return {"message": "Combat ended"}

@app.post("/dm-assistant/scenarios")
def get_scenario_suggestions(
    campaign_id: int,
    scenario_request: ScenarioRequest,
    db: Session = Depends(get_db)
):
    engine = GameEngine(db)
    characters = engine.get_characters(campaign_id)
    
    char_info = [
        {
            "name": char.name,
            "race": char.race,
            "char_class": char.char_class,
            "level": char.level,
            "personality_traits": char.personality_traits
        }
        for char in characters
    ]
    
    assistant = DMAssistant()
    suggestions = assistant.suggest_scenarios(scenario_request.context, char_info)
    
    return {"suggestions": suggestions}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
