import pygame
from settings import *
from sprites import Generic
from support import import_folder
from timer import Timer


class BuildingCreator(pygame.sprite.Sprite):
    def __init__(self, player, groups, market):
        super().__init__()
        self.recipies = RECIPIES
        self.player = player
        self.groups = groups
        self.market = market

        # buildings assets
        self.assets = {'export_box': ''}
        self.import_assets()

        # create export box
        self.create_export_box()

    def import_assets(self):
        for asset in self.assets.keys():
            full_path = '../graphics/buildings/' + asset
            self.assets[asset] = import_folder(full_path)

    def create_export_box(self):
        self.export_box = ExportBox((ZONE_WIDTH * MAP_WIDTH / 2, ZONE_HEIGHT * MAP_HEIGHT / 2 + 100),
                                    self.assets['export_box'][0], self.assets['export_box'], self.groups,
                                    LAYERS['main'], None, self.market)


class Building(Generic):
    def __init__(self, pos, surf, sprites, groups, z, recipes):
        super().__init__(pos, surf, groups, z)
        self.sprites = sprites
        self.frame_index = 0
        self.recipies = recipes


class ExportBox(Building):
    def __init__(self, pos, surf, sprites, groups, z, recipes, market):
        super().__init__(pos, surf, sprites, groups, z, recipes)
        self.market = market

    def interact(self, player):
        change = False
        if not player.timers['resource_input'].active:
            if player.selected_resource in self.market.demand and self.market.demand[player.selected_resource] > 0:
                player.timers['resource_input'].activate()
                self.market.demand[player.selected_resource] -= 1
                player.inventory[player.selected_resource] -= 1
                if player.inventory[player.selected_resource] == 0:
                    del player.inventory[player.selected_resource]
                    change = True
                if self.market.demand[player.selected_resource] == 0:
                    del self.market.demand[player.selected_resource]
            if change:
                player.selected_resource = ''
