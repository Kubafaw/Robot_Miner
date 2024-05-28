import pygame
from settings import *
from support import import_folder


class Overlay:
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # import
        self.import_assets()

        # cursor
        self.cursor_frame_index = 0

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

            # check for collision
            for rock in self.player.mineable.sprites():
                if rock.hitbox_rect.colliderect(mining_rect):
                    rock.damage(self.player)

