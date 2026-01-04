from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    party_size = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    characters = relationship("Character", back_populates="campaign", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="campaign", cascade="all, delete-orphan")
    combat_state = relationship("CombatState", back_populates="campaign", uselist=False, cascade="all, delete-orphan")

class Character(Base):
    __tablename__ = "characters"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    name = Column(String, nullable=False)
    race = Column(String, nullable=False)
    char_class = Column(String, nullable=False)
    level = Column(Integer, default=1)
    
    strength = Column(Integer, default=10)
    dexterity = Column(Integer, default=10)
    constitution = Column(Integer, default=10)
    intelligence = Column(Integer, default=10)
    wisdom = Column(Integer, default=10)
    charisma = Column(Integer, default=10)
    
    max_hp = Column(Integer, nullable=False)
    current_hp = Column(Integer, nullable=False)
    armor_class = Column(Integer, default=10)
    
    personality_traits = Column(JSON)
    background = Column(Text)
    inventory = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    campaign = relationship("Campaign", back_populates="characters")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=True)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(String, default="narrative")
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    campaign = relationship("Campaign", back_populates="messages")

class CombatState(Base):
    __tablename__ = "combat_state"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False, unique=True)
    is_active = Column(Boolean, default=False)
    current_turn = Column(Integer, default=0)
    round_number = Column(Integer, default=1)
    initiative_order = Column(JSON, default=list)
    
    campaign = relationship("Campaign", back_populates="combat_state")
