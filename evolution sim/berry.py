import pygame
import math
import random

screen_widthB = 1360
screen_heightB = 980
screenB = pygame.display.set_mode((screen_widthB, screen_heightB))

class Berry:
    def __init__(self,
                 regen_time,
                 available,
                 size,
                 cx,
                 cy):
        self.regen_time = regen_time
        self.available = available
        self.size = size
        self.cx = cx
        self.cy = cy

    def create(self):
        if self.available == True:
            pygame.draw.circle(screenB, 'pink', (self.cx, self.cy), self.size)

    def reset(self,count):
        if self.available == False:
            count+=1
            if count >= self.regen_time:
                self.available = True
                count = 0
        return count