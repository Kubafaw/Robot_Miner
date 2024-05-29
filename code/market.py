import pygame
from settings import *
from random import randint


class Market(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.create_demand()

    def create_demand(self):
        self.demand = {}
        for ore in ORES:
            self.demand[ore] = randint(1, 20)

    def satisfy_demand(self, resource, amount):
        if resource in self.demand.keys():
            self.demand[resource] -= amount
            return True
        else:
            return False

    def check_if_fullified(self):
        still_needed = 0
        for value in self.demand.values():
            if value > 0:
                still_needed += 1

        if still_needed == 0:
            self.create_demand()

