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
    def Ishungry(self):
        if self.current_hunger < self.max_hunger / 2:
            return True
        else:
            return False



    def selectlocation(self):
        hungry = self.Ishungry()
        if not hungry:
            print('not hungry')
            locationX = random.randint(self.size,screen_width-self.size)
            locationY = random.randint(self.size,screen_height-self.size)
        if hungry:
            print('hungry')
            #enter look for food state
            for berry in self.berries:
                # Check if the berry is available
                if berry[0].available:
                    distance = calculate_distance(self.cx, self.cy, berry[0].cx, berry[0].cy)
                    # If close enough to see
                    if distance < self.size + berry[0].size + self.sight:
                        locationX = berry[0].cx
                        locationY = berry[0].cy
                        print('going towards berry')
                    else:
                        locationX = random.randint(self.size, screen_width - self.size)
                        locationY = random.randint(self.size, screen_height - self.size)
                        print('no berry')


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