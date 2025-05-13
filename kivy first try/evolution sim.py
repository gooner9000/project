import pygame

class Slime:
    def __init__(self,
                 speed,
                 max_hunger,
                 colour,
                 size,
                 agression):
        self.speed = speed
        self.max_hunger = max_hunger
        self.colour = colour
        self.size = size
        self.agression = agression
    def create(self):
        pygame.draw.
