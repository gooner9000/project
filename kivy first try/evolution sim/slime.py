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
                 max_hunger,
                 metabolism,
                 current_hunger,
                 colour,
                 size,
                 agression,
                 sight,
                 cx,
                 cy,
                 dead,
                 berries):
        self.speed = speed
        self.max_hunger = max_hunger
        self.metabolism = metabolism
        self.current_hunger = current_hunger
        self.colour = colour
        self.size = size
        self.agression = agression
        self.sight = sight
        self.cx = cx
        self.cy = cy
        self.posX,self.posY = self.selectlocation()
        self.dead = dead
        self.berries = berries



    #function to create slimes at start
    def create(self):

        pygame.draw.circle(screen,self.colour,(self.cx,self.cy),self.size)
        #visiulize where its going to go
        pygame.draw.line(screen, "white", (self.cx, self.cy), (self.posX, self.posY), 1)
        #visualize sight
        pygame.draw.circle(screen, self.colour, (self.cx, self.cy), self.sight, 1)
    def Ishungry(self):
        if self.current_hunger < self.max_hunger / 2:
            return True
        else:
            return False

    def Checkforberry(self,berry):

        if berry[0].available:
            distance = calculate_distance(self.cx, self.cy, berry[0].cx, berry[0].cy)
            # If close enough to see
            if distance < self.sight:

                return True
        return False
    def selectlocation(self):
        hungry = self.Ishungry()
        locationX = random.randint(self.size, screen_width - self.size)
        locationY = random.randint(self.size, screen_height - self.size)
        if not hungry:
            print('not hungry')
            return locationX, locationY
        else:
            print('hungry')
            #enter look for food state
            for berry in self.berries:
                if self.Checkforberry(berry) == True:
                    locationX = berry[0].cx
                    locationY = berry[0].cy
                    print('going towards berry')
                    break




        return locationX,locationY


    def die(self):
        if self.current_hunger <= 0:

            return True
        return False


    def lose_hunger(self,count):
        count += 1
        if count >= self.metabolism:
            self.dead = self.die()
            self.current_hunger -= 1
            print(f"current hunger: {self.current_hunger}")
            count = 0
        return count

    def move(self):
        #check to interupt
        if self.Ishungry():
            is_targeting_food = False
            #check if already targeting
            for berry in self.berries:
                if berry[0].available and self.posX == berry[0].cx and self.posY == berry[0].cy:
                    is_targeting_food = True
                    break
            #if not then target
            if not is_targeting_food:
                for berry in self.berries:
                    if self.Checkforberry(berry):
                        print("interupted going towards berry")
                        self.posX = berry[0].cx
                        self.posY = berry[0].cy
                        break

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

    def eat(self):
        for berry in self.berries:
            # Check if the berry is available
            if berry[0].available:
                distance = calculate_distance(self.cx, self.cy, berry[0].cx, berry[0].cy)
                # If close enough to eat
                if distance < self.size + berry[0].size:
                    self.current_hunger += 5
                    # Cap hunger at max_hunger
                    if self.current_hunger > self.max_hunger:
                        self.current_hunger = self.max_hunger
                    berry[0].available = False  # The slime eats the berry
                    print(f"Yum! Hunger is now {self.current_hunger}")
                    break  # Stop checking after eating one berry per frame