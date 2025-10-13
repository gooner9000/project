import random
import math
import pygame

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
screen_width = 1360
screen_height = 980
screen = pygame.display.set_mode((screen_width, screen_height))
class Slime:
    def __init__(self,
                 speed,
                 max_calories,
                 metabolism,
                 current_calories,
                 hunger_num,
                 colour,
                 size,
                 agression,
                 sight,
                 cx,
                 cy,
                 dead):
        self.speed = speed
        self.max_calories = max_calories
        self.metabolism = metabolism
        self.current_calories = current_calories
        self.hunger = hunger_num
        self.colour = colour
        self.size = size
        self.agression = agression
        self.sight = sight
        self.cx = cx
        self.cy = cy
        self.posX,self.posY = self.selectlocation()
        self.dead = dead



    #function to create slimes at start
    def create(self):

        pygame.draw.circle(screen,self.colour,(self.cx,self.cy),self.size)

    def selectlocation(self,berries):
        if self.calories <= self.max_calories:
            for berry in berries:


        locationX = random.randint(self.size,screen_width-self.size)
        locationY = random.randint(self.size,screen_height-self.size)

        return locationX,locationY


    def die(self):
        if self.current_calories <= 0:

            return True
        return False


    def lose_hunger(self,count):
        count += 1
        if count >= self.metabolism:
            self.dead = self.die()
            self.current_calories -= 1
            print(f"current hunger: {self.current_calories}")
            count = 0
        return count

    def move(self):


        #calculate distance
        dx = self.posX - self.cx
        dy = self.posY - self.cy
        distance = math.sqrt(dx ** 2 + dy ** 2)

    # If closer than one step, snap to target and pick new
        if distance < self.speed:
            wait = True
            while wait == True:
                for i in range(0,random.randint(100000,100000)):
                    wait = False
            self.cx = self.posX
            self.cy = self.posY
            self.posX,self.posY = self.selectlocation()

        else:
                #move the circle
             if distance != 0:
                move_x = (dx / distance) * self.speed
                move_y = (dy / distance) * self.speed

                self.cx += move_x
                self.cy += move_y

    def eat(self, berries):
        for berry in berries:
            # Check if the berry is available
            if berry[0].available:
                distance = calculate_distance(self.cx, self.cy, berry[0].cx, berry[0].cy)
                # If close enough to eat
                if distance < self.size + berry[0].size:
                    self.current_calories += 5
                    # Cap hunger at max_hunger
                    if self.current_calories > self.max_calories:
                        self.current_calories = self.max_calories
                    berry[0].available = False  # The slime eats the berry
                    print(f"Yum! Hunger is now {self.current_calories}")
                    break  # Stop checking after eating one berry per frame