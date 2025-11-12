from enum import Enum


class Difficulty(Enum):
    LEVEL_1 = 5    # Slowest
    LEVEL_2 = 7
    LEVEL_3 = 9
    LEVEL_4 = 11
    LEVEL_5 = 13
    LEVEL_6 = 15
    LEVEL_7 = 17
    LEVEL_8 = 20   # Fastest


class GameMode(Enum):
    CLASSIC = "Classic"           # Can go through walls, only dies when hitting body
    MODERN = "Modern"             # Cannot go through walls, dies when hitting wall or body
    CAMPAIGN = "Campaign"         # Level-based mode with obstacles, 5 levels total


DIFFICULTY_NAMES = {
    Difficulty.LEVEL_1: "Level 1",
    Difficulty.LEVEL_2: "Level 2",
    Difficulty.LEVEL_3: "Level 3",
    Difficulty.LEVEL_4: "Level 4",
    Difficulty.LEVEL_5: "Level 5",
    Difficulty.LEVEL_6: "Level 6",
    Difficulty.LEVEL_7: "Level 7",
    Difficulty.LEVEL_8: "Level 8",
}

GAMEMODE_DESCRIPTIONS = {
    GameMode.CLASSIC: "Go through walls, die on body hit",
    GameMode.MODERN: "Die on walls and body hit",
    GameMode.CAMPAIGN: "5 levels with obstacles and portals",
}
