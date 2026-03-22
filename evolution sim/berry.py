import pygame
import math
import random

#set the size of the screen
screen_widthB = 1360
screen_heightB = 980
screenB = pygame.display.set_mode((screen_widthB, screen_heightB))

class Berry:
    """ description: class that creates and handles the berry object

        attributes: regen_time = time it takes for a berry to become available again
                    available = true or false tells slimes if it can be eaten or not and if it should be drawn to the screen
                    size = radius of berry
                    cx,cy = current position of the berry"""
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
        """draws the berry to the screen if it is available"""
        if self.available == True:
            pygame.draw.circle(screenB, 'pink', (self.cx, self.cy), self.size)

    def reset(self,count):
        """starts the counter to make the berry available again once it has been eaten"""
        if self.available == False:
            count+=1
            if count >= self.regen_time:
                self.available = True
                count = 0
        return count