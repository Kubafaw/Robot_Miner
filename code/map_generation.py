import pygame
from settings import *
from random import randint
from support import import_folder
from sprites import OreRock
from timer import Timer


class Core(pygame.sprite.Sprite):
    def __init__(self, zones, amounts, groups):
        super().__init__()
        self.zones = zones
        self.amounts = amounts
        self.groups = groups

        self.import_assets()
        self.create_zones()

    def import_assets(self):
        self.ores = {'iron': [], 'coal': [], 'copper': []}

        for ore in self.ores.keys():
            full_path = '../graphics/ores/' + ore
            self.ores[ore] = import_folder(full_path)

    def create_zones(self):
        # get areas distribution and crate them
        self.areas = []
        self.areas_created = []
        for i in range(MAP_WIDTH):
            self.areas += [[]]
            for j in range(MAP_HEIGHT):
                self.areas[i] += ['0']
        self.areas[int(MAP_WIDTH/2)][int(MAP_HEIGHT/2)] = 'empty'
        self.areas_created += [Area((int(MAP_WIDTH/2) * ZONE_WIDTH, int(MAP_HEIGHT/2) * ZONE_HEIGHT), self.groups, 'none',
                                    'none', 'empty')]
        k = 0
        for amount in self.amounts:
            for _ in range(amount):
                i = randint(0, MAP_WIDTH - 1)
                j = randint(0, MAP_HEIGHT - 1)
                while self.areas[i][j] != '0':
                    i = randint(0, MAP_WIDTH - 1)
                    j = randint(0, MAP_HEIGHT - 1)
                self.areas[i][j] = self.zones[k]
                self.areas_created += [Area((i * ZONE_WIDTH, j * ZONE_HEIGHT), self.groups, self.zones[k],
                                       self.ores[self.zones[k]], 'rocky')]
            k += 1
        for i in range(MAP_WIDTH):
            for j in range(MAP_HEIGHT):
                if self.areas[i][j] == '0':
                    self.areas[i][j] = 'empty'
                    self.areas_created += [Area((i * ZONE_WIDTH, j * ZONE_HEIGHT), self.groups, 'none',
                                                'none', 'empty')]


class Area(pygame.sprite.Sprite):
    def __init__(self, pos, groups, resource, sprites, type):
        super().__init__((groups[0], groups[1]))
        self.pos = pos
        self.groups = groups
        self.resource = resource
        self.sprites = sprites
        self.z = LAYERS['landscape']
        self.nodes = 0
        self.max_nodes = NODES_PER_ZONE
        self.type = type

        # set surface
        self.image = pygame.Surface((ZONE_WIDTH, ZONE_HEIGHT))
        self.image.fill(AREAS_BACKGROUND[type])
        self.rect = self.image.get_rect(topleft=pos)

        # resurces area
        self.area = []
        for i in range(int(ZONE_WIDTH / 96)):
            self.area += [[]]
            for j in range(int(ZONE_HEIGHT / 96)):
                self.area[i] += ['0']

        # generate starting rocks
        if self.resource != 'none':
            self.generate_nodes(6)

        # timer
        self.res_reg_timer = Timer(RESOURCE_REGENERATION)
        self.res_reg_timer.activate()

    def generate_nodes(self, amount):
        for _ in range(amount):
            i = randint(0, int(ZONE_WIDTH / 96)-1)
            j = randint(0, int(ZONE_HEIGHT / 96)-1)
            while self.area[i][j] != '0':
                i = randint(0, int(ZONE_WIDTH / 96)-1)
                j = randint(0, int(ZONE_HEIGHT / 96)-1)
            self.area[i][j] = '1'
            self.nodes += 1
            k = randint(0, 2)
            OreRock((self.rect.left + i * 96, self.rect.top + j * 96), self.sprites[k],
                    self.sprites, (self.groups[0], self.groups[2]), self.resource, LAYERS['main'], k,
                    self, (i, j))

    def update(self, dt):
        if self.resource != 'none':
            self.res_reg_timer.update()
            if not self.res_reg_timer.active and self.nodes < self.max_nodes:
                self.generate_nodes(1)
                self.res_reg_timer.activate()
