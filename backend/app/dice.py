import random
from typing import List, Tuple

class DiceRoller:
    @staticmethod
    def roll(sides: int, count: int = 1) -> Tuple[int, List[int]]:
        rolls = [random.randint(1, sides) for _ in range(count)]
        return sum(rolls), rolls
    
    @staticmethod
    def d4(count: int = 1) -> Tuple[int, List[int]]:
        return DiceRoller.roll(4, count)
    
    @staticmethod
    def d6(count: int = 1) -> Tuple[int, List[int]]:
        return DiceRoller.roll(6, count)
    
    @staticmethod
    def d8(count: int = 1) -> Tuple[int, List[int]]:
        return DiceRoller.roll(8, count)
    
    @staticmethod
    def d10(count: int = 1) -> Tuple[int, List[int]]:
        return DiceRoller.roll(10, count)
    
    @staticmethod
    def d12(count: int = 1) -> Tuple[int, List[int]]:
        return DiceRoller.roll(12, count)
    
    @staticmethod
    def d20(count: int = 1) -> Tuple[int, List[int]]:
        return DiceRoller.roll(20, count)
    
    @staticmethod
    def d100(count: int = 1) -> Tuple[int, List[int]]:
        return DiceRoller.roll(100, count)
    
    @staticmethod
    def ability_score() -> int:
        rolls = [random.randint(1, 6) for _ in range(4)]
        rolls.sort(reverse=True)
        return sum(rolls[:3])
    
    @staticmethod
    def modifier(score: int) -> int:
        return (score - 10) // 2
