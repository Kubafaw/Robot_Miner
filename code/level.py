import pygame
from settings import *
from player import Player
from map_generation import Core
from overlay import Overlay
from sprites import OreRock
from buildings import BuildingCreator
from market import Market


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()
        self.mineable = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.areas = pygame.sprite.Group()
        self.buildings = pygame.sprite.Group()

        self.setup()

    def setup(self):
        self.player = Player(
            pos=(ZONE_WIDTH * MAP_WIDTH / 2, ZONE_HEIGHT * MAP_HEIGHT / 2),
            group=self.all_sprites,
            mineable=self.mineable,
            collision_sprites=self.collision_sprites,
            buildings=self.buildings)

        # market
        self.market = Market()

        # building creator
        self.building_creator = BuildingCreator(self.player, (self.all_sprites, self.buildings), self.market)

        # overlay
        self.overlay = Overlay(self.player, self.market)

        # map generation
        self.core = Core(['iron', 'copper', 'coal'], [20, 20, 20],
                         (self.all_sprites, self.areas, self.mineable))

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)
        self.market.check_if_fullified()

        self.overlay.display(dt)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
                    # pygame.draw.rect(self.display_surface, 'green', offset_rect, 5)

                    if sprite == OreRock:
                        offset_rect = sprite.hitbox_rect.copy()
                        offset_rect.center -= self.offset
                        # pygame.draw.rect(self.display_surface, 'green', offset_rect, 5)

