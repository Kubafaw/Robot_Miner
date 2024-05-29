import pygame
from settings import *
from support import import_folder


class Overlay:
    def __init__(self, player, market):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.market = market

        # import
        self.import_assets()

        # cursor
        self.cursor_frame_index = 0

        # inventory
        self.inventory = {'slot': '', 'selected': '', 'iron': '', 'copper': '', 'coal': ''}
        self.setup_inventory()

    def import_assets(self):
        self.animations = {}
        for tool in self.player.tools:
            self.animations[tool] = []

        for animation in self.animations.keys():
            full_path = '../graphics/overlay/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        if self.player.using_tool:
            self.cursor_frame_index += 16 * dt

        if self.cursor_frame_index >= len(self.animations[self.player.selected_tool]):
            self.cursor_frame_index = 0

        cursor_surf = self.animations[self.player.selected_tool][int(self.cursor_frame_index)]
        coordinates = pygame.mouse.get_pos()
        self.display_surface.blit(cursor_surf, cursor_surf.get_rect(midleft=coordinates))

    def display(self, dt):
        self.draw_inventory()
        self.draw_market_demand()
        self.animate(dt)
        self.tool_usage()

    def tool_usage(self):
        if self.player.using_tool:
            mining_pos = pygame.mouse.get_pos()
            mining_surf = self.animations[self.player.selected_tool][int(self.cursor_frame_index)]
            image = pygame.Surface((mining_surf.get_rect().width - 50, mining_surf.get_rect().height - 50))
            mining_rect = (image.get_rect(center=mining_pos))

            # debug
            # image.fill('red')
            # self.display_surface.blit(image, mining_rect)

            mining_rect.x = self.player.rect.x + mining_pos[0] - 920
            mining_rect.y = self.player.rect.y + mining_pos[1] - 500

            # check for collision 'drill'
            if self.player.selected_tool == 'drill':
                for rock in self.player.mineable.sprites():
                    if rock.hitbox_rect.colliderect(mining_rect):
                        rock.damage(self.player)

            # check for collision 'arm'
            if self.player.selected_tool == 'arm':
                for building in self.player.buildings.sprites():
                    if building.rect.colliderect(mining_rect):
                        building.interact(self.player)

    def setup_inventory(self):
        for picture in self.inventory.keys():
            full_path = '../graphics/overlay/inventory/' + picture
            self.inventory[picture] = pygame.image.load(f'{full_path}.png')

    def draw_inventory(self):
        k = 0
        for i in range(8):
            inventory_surf = self.inventory['slot']
            inventory_rect = inventory_surf.get_rect(center=(525 + k * 128, SCREEN_HEIGHT - 200))
            self.display_surface.blit(inventory_surf, inventory_rect)
            if self.player.selected_inventory_slot == i:
                inventory_surf = self.inventory['selected']
                inventory_rect = inventory_surf.get_rect(center=(525 + k * 128, SCREEN_HEIGHT - 200))
                self.display_surface.blit(inventory_surf, inventory_rect)
            k += 1

        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        k = 0
        for item in self.player.inventory.keys():
            inventory_surf = self.inventory[item]
            inventory_rect = inventory_surf.get_rect(center=(525 + k * 128, SCREEN_HEIGHT - 200))
            self.display_surface.blit(inventory_surf, inventory_rect)
            text_surf = my_font.render(str(self.player.inventory[item]), False, (0, 0, 0))
            text_rect = text_surf.get_rect(center=(525 + k * 128, SCREEN_HEIGHT - 130))
            self.display_surface.blit(text_surf, text_rect)
            k += 1

    def draw_market_demand(self):
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        k = 0
        for item in self.market.demand.keys():
            inventory_surf = self.inventory['slot']
            inventory_rect = inventory_surf.get_rect(center=(SCREEN_WIDTH - 280, SCREEN_HEIGHT - 700 + k * 150))
            self.display_surface.blit(inventory_surf, inventory_rect)

            inventory_surf = self.inventory[item]
            inventory_rect = inventory_surf.get_rect(center=(SCREEN_WIDTH - 280, SCREEN_HEIGHT - 700 + k * 150))
            self.display_surface.blit(inventory_surf, inventory_rect)
            text_surf = my_font.render(str(self.market.demand[item]), False, (0, 0, 0))
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH - 280, SCREEN_HEIGHT - 640 + k * 150))
            self.display_surface.blit(text_surf, text_rect)
            k += 1

