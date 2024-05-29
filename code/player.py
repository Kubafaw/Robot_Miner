import pygame
from settings import *
from support import import_folder
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, mineable, collision_sprites, buildings):
        super().__init__(group)

        self.import_assets()
        self.status = 'right'
        self.frame_index = 0
        self.mineable = mineable
        self.buildings = buildings

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['player']

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 400

        # collision
        self.hitbox = self.rect.copy().inflate((-126, -70))
        self.collision_sprites = collision_sprites

        # tools
        self.tools = ['drill', 'arm']
        self.using_tool = False
        self.selected_tool = 'drill'
        self.tool_index = 0
        self.selected_resource = ''

        # timers
        self.timers = {
            'tool_use': Timer(300),
            'tool_change': Timer(300),
            'inventory_change': Timer(200),
            'resource_input': Timer(100)
        }

        # inventory
        self.inventory_slots = 8
        self.used_inventory_slots = 0
        self.inventory = {}
        self.selected_inventory_slot = 0

    def import_assets(self):
        self.animations = {'left': [], 'right': [], 'left_idle': [], 'right_idle': []}

        for animation in self.animations.keys():
            full_path = '../graphics/player/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 16 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def get_status(self):

        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.y = 0
        self.direction.x = 0

        # directions
        if keys[pygame.K_w]:
            self.direction.y -= 1
        if keys[pygame.K_s]:
            self.direction.y += 1

        if keys[pygame.K_d]:
            self.direction.x += 1
        if keys[pygame.K_a]:
            self.direction.x -= 1

        if self.direction.x > 0:
            self.status = 'right'
        elif self.direction.x < 0:
            self.status = 'left'
        elif self.direction.y != 0:
            self.status = 'right'

        # change tool
        if not self.timers['tool_change'].active:
            self.timers['tool_change'].activate()
            if keys[pygame.K_q]:
                self.tool_index -= 1
            if keys[pygame.K_e]:
                self.tool_index += 1

            if self.tool_index >= len(self.tools):
                self.tool_index = 0
            if self.tool_index < 0:
                self.tool_index = len(self.tools) - 1

            self.selected_tool = self.tools[self.tool_index]

        # tool usage
        if pygame.mouse.get_pressed()[0]:
            self.using_tool = True
        else:
            self.using_tool = False

        # cycle through inventory
        if not self.timers['inventory_change'].active:
            self.timers['inventory_change'].activate()
            if keys[pygame.K_k]:
                self.selected_inventory_slot -= 1
            elif keys[pygame.K_l]:
                self.selected_inventory_slot += 1

            if self.selected_inventory_slot >= self.inventory_slots:
                self.selected_inventory_slot = 0
            if self.selected_inventory_slot < 0:
                self.selected_inventory_slot = self.inventory_slots - 1

            k = 0
            self.selected_resource = ''
            for key in self.inventory.keys():
                if k == self.selected_inventory_slot:
                    self.selected_resource = key
                k += 1
            print(self.selected_resource)

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def move(self, dt):
        if self.direction != [0, 0]:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt

        # check for the map edge
        if self.pos.x <= 0:
            self.pos.x = 0
        if self.pos.x >= ZONE_WIDTH * MAP_WIDTH:
            self.pos.x = ZONE_WIDTH * MAP_WIDTH

        if self.pos.y <= 0:
            self.pos.y = 0
        if self.pos.y >= ZONE_HEIGHT * MAP_HEIGHT:
            self.pos.y = ZONE_HEIGHT * MAP_HEIGHT

        # position update
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.move(dt)
        self.animate(dt)

        # debug
        # print(self.inventory)
