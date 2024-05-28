from pygame.math import Vector2

# ores
ORES = [
    'iron',
    'copper',
    'coal'
]

# zone
ZONE_WIDTH = 480
ZONE_HEIGHT = 480
NODES_PER_ZONE = 8
RESOURCE_REGENERATION = 10000

# areas backgrounds
AREAS_BACKGROUND = {
    'rocky': 'grey45',
    'woods': 'green4',
    'empty': 'darkgoldenrod'
}

# map
MAP_WIDTH = 10  # in zones
MAP_HEIGHT = 10  # in zones

# screen
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# overlay positions
OVERLAY_POSITIONS = {
}

LAYERS = {
    'landscape': 1,
    'main': 2,
    'player': 3,
    'overlay': 4,
    'cursor': 5
}
