import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z


class OreRock(Generic):
    def __init__(self, pos, surf, sprites, groups, ore, z, frame_index, area, coordinates):
        super().__init__(pos, surf, groups, z)
        self.ore = ore
        self.sprites = sprites
        self.frame_index = frame_index
        self.area = area
        self.coordinates = coordinates
        self.hitbox_rect = self.rect.copy()
        self.hitbox_rect.h -= 50
        self.hitbox_rect.w -= 30
        self.hitbox_rect.y += 40

    def update(self, dt):
        pass

    def damage(self, player):
        if not player.timers['tool_use'].active:
            player.timers['tool_use'].activate()
            self.frame_index += 1
            if self.ore in player.inventory.keys():
                player.inventory[self.ore] += 1
            else:
                player.inventory[self.ore] = 1
                player.used_inventory_slots += 1
            if self.frame_index >= len(self.sprites):
                self.area.nodes -= 1
                self.area.area[self.coordinates[0]][self.coordinates[1]] = '0'
                self.kill()
            else:
                self.image = self.sprites[self.frame_index]
