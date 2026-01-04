import random
from typing import Dict, List
from app.dice import DiceRoller

class CharacterGenerator:
    RACES = [
        "Human", "Elf", "Dwarf", "Halfling", "Dragonborn",
        "Gnome", "Half-Elf", "Half-Orc", "Tiefling"
    ]
    
    CLASSES = [
        "Fighter", "Wizard", "Cleric", "Rogue", "Ranger",
        "Paladin", "Bard", "Barbarian", "Warlock", "Monk"
    ]
    
    PERSONALITIES = [
        "brave", "cautious", "greedy", "noble", "curious",
        "sarcastic", "optimistic", "pessimistic", "loyal", "ambitious"
    ]
    
    FIRST_NAMES = {
        "Human": ["Aldric", "Brenna", "Cedric", "Diana", "Erik", "Fiona"],
        "Elf": ["Aelindra", "Thalion", "Sylvara", "Eldrin", "Lyria", "Caelum"],
        "Dwarf": ["Thorin", "Brunhilde", "Gimli", "Helga", "Balin", "Freya"],
        "Halfling": ["Bilbo", "Rosie", "Pippin", "Daisy", "Merry", "Lily"],
        "Dragonborn": ["Drax", "Sora", "Kriv", "Nala", "Balasar", "Mishann"],
        "Gnome": ["Fizban", "Tilly", "Glim", "Nissa", "Boddynock", "Oda"],
        "Half-Elf": ["Tanis", "Arianna", "Gareth", "Elara", "Sorin", "Mira"],
        "Half-Orc": ["Grok", "Shava", "Thokk", "Yarga", "Dench", "Krazz"],
        "Tiefling": ["Zariel", "Lilith", "Azazel", "Mephista", "Damien", "Seraphine"]
    }
    
    CLASS_HP_DICE = {
        "Fighter": 10, "Wizard": 6, "Cleric": 8, "Rogue": 8,
        "Ranger": 10, "Paladin": 10, "Bard": 8, "Barbarian": 12,
        "Warlock": 8, "Monk": 8
    }
    
    @staticmethod
    def generate_character() -> Dict:
        race = random.choice(CharacterGenerator.RACES)
        char_class = random.choice(CharacterGenerator.CLASSES)
        name = random.choice(CharacterGenerator.FIRST_NAMES[race])
        
        str_score = DiceRoller.ability_score()
        dex_score = DiceRoller.ability_score()
        con_score = DiceRoller.ability_score()
        int_score = DiceRoller.ability_score()
        wis_score = DiceRoller.ability_score()
        cha_score = DiceRoller.ability_score()
        
        hp_dice = CharacterGenerator.CLASS_HP_DICE[char_class]
        max_hp = hp_dice + DiceRoller.modifier(con_score)
        
        ac = 10 + DiceRoller.modifier(dex_score)
        
        personality = random.sample(CharacterGenerator.PERSONALITIES, 2)
        
        background = CharacterGenerator._generate_background(name, race, char_class, personality)
        
        return {
            "name": name,
            "race": race,
            "char_class": char_class,
            "level": 1,
            "strength": str_score,
            "dexterity": dex_score,
            "constitution": con_score,
            "intelligence": int_score,
            "wisdom": wis_score,
            "charisma": cha_score,
            "max_hp": max_hp,
            "current_hp": max_hp,
            "armor_class": ac,
            "personality_traits": personality,
            "background": background,
            "inventory": CharacterGenerator._starting_equipment(char_class)
        }
    
    @staticmethod
    def _generate_background(name: str, race: str, char_class: str, personality: List[str]) -> str:
        backgrounds = [
            f"{name} is a {personality[0]} {race} {char_class} who seeks adventure and glory.",
            f"A {personality[1]} {race}, {name} became a {char_class} to protect their village.",
            f"{name}, a {personality[0]} {race} {char_class}, is driven by a mysterious past.",
            f"Once a simple {race}, {name} discovered their talent as a {char_class} and embraced destiny."
        ]
        return random.choice(backgrounds)
    
    @staticmethod
    def _starting_equipment(char_class: str) -> List[str]:
        equipment = {
            "Fighter": ["Longsword", "Shield", "Chain Mail", "Backpack", "50 gold"],
            "Wizard": ["Spellbook", "Quarterstaff", "Component Pouch", "Scholar's Pack", "30 gold"],
            "Cleric": ["Mace", "Scale Mail", "Shield", "Holy Symbol", "Priest's Pack", "25 gold"],
            "Rogue": ["Shortsword", "Shortbow", "Leather Armor", "Thieves' Tools", "40 gold"],
            "Ranger": ["Longbow", "Shortsword", "Leather Armor", "Explorer's Pack", "35 gold"],
            "Paladin": ["Longsword", "Shield", "Chain Mail", "Holy Symbol", "20 gold"],
            "Bard": ["Rapier", "Lute", "Leather Armor", "Entertainer's Pack", "45 gold"],
            "Barbarian": ["Greataxe", "Handaxe", "Explorer's Pack", "30 gold"],
            "Warlock": ["Light Crossbow", "Component Pouch", "Leather Armor", "Scholar's Pack", "25 gold"],
            "Monk": ["Shortsword", "Dart (10)", "Explorer's Pack", "15 gold"]
        }
        return equipment.get(char_class, ["Basic Equipment", "20 gold"])
    
    @staticmethod
    def generate_party(size: int) -> List[Dict]:
        return [CharacterGenerator.generate_character() for _ in range(size)]
