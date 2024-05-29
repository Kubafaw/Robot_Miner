from pygame.math import Vector2

# ores
ORES = [
    'iron',
    'copper',
    'coal'
]

# zone
ZONE_WIDTH = 480  # pix
ZONE_HEIGHT = 480  # pix
NODES_PER_ZONE = 8
RESOURCE_REGENERATION = 10000  # ms

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
SCREEN_WIDTH = 1920  # pix
SCREEN_HEIGHT = 1080  # pix

LAYERS = {  # for displaying layered view
    'landscape': 1,
    'main': 2,
    'player': 3,
    'overlay': 4,
    'cursor': 5
}

RECIPIES = {
    'smelter': {
        'iron bar': ['iron'],
        'copper bar': ['copper']}
}
