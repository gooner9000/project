import math
import pygame
import random
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
def check_collision(x1,y1,x2,y2):
    if calculate_distance(x1,y1,x2,y2) <= 3:
        return True
    return False
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
        self.dead = dead
        self.berries = berries
        self.Can_copy = False
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
        self.posX,self.posY = self.selectlocation([])



    #function to create slimes at start
    def create(self):

        pygame.draw.circle(screen,self.colour,(self.cx,self.cy),self.size)
        #visiulize where its going to go
        #pygame.draw.line(screen, "white", (self.cx, self.cy), (self.posX, self.posY), 1)
        #visualize sight
        #pygame.draw.circle(screen, self.colour, (self.cx, self.cy), self.sight, 1)
    def Ishungry(self):
        if self.current_hunger < self.max_hunger * 0.5:
            return True
        else:
            return False
    def Reproduce(self,slime):
        print("reproducing")

        self.Can_copy = True
        partner = slime
        return partner
    def Canreproduce(self):
        if self.current_hunger >= self.max_hunger * 0.7:
            print("can reproduce")
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
    def Checkforslime(self,slime):
        distance = calculate_distance(self.cx, self.cy, slime[0].cx, slime[0].cy)
        if distance < self.sight and slime[0] is not self:
            return True
        return False
    def selectlocation(self,slimes):
        hungry = self.Ishungry()
        repro_able = self.Canreproduce()
        locationX = random.randint(self.size, screen_width - self.size)
        locationY = random.randint(self.size, screen_height - self.size)
        if not hungry and not repro_able:
            print('not hungry')
            print('cant reproduce')
            return locationX, locationY
        elif hungry:
            print('hungry')
            #enter look for food state
            for berry in self.berries:
                if self.Checkforberry(berry) == True:
                    locationX = berry[0].cx
                    locationY = berry[0].cy
                    print('going towards berry')
                    break
        elif repro_able:
            print('can reproduce')
            #enter look for slime state
            for slime in slimes:
                if self.Checkforslime(slime) == True and slime[0].Canreproduce():
                    locationX = slime[0].cx
                    locationY = slime[0].cy
                    print('going towards slime')
                    if check_collision(self.cx,self.cy,slime[0].cx,slime[0].cy):
                        self.Reproduce(slime[0])
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

    def move(self,slimes):
        #check to interupt
        if self.Ishungry():
            is_targeting_food = False
            #check if already targeting food
            for berry in self.berries:
                if berry[0].available and self.posX == berry[0].cx and self.posY == berry[0].cy:
                    is_targeting_food = True
                    break
            #if not then target food
            if not is_targeting_food:
                for berry in self.berries:
                    if self.Checkforberry(berry):
                        print("interupted going towards berry")
                        self.posX = berry[0].cx
                        self.posY = berry[0].cy
                        break
        if self.Canreproduce():
            is_targeting_slime = False
            #check if already targeting slime
            for slime in slimes:
                if self.posX == slime[0].cx and self.posY == slime[0].cy:
                    print("is already targeting")
                    is_targeting_food = True
                    if check_collision(self.cx,self.cy,slime[0].cx,slime[0].cy):
                        partner = self.Reproduce(slime[0])
                        return partner
                    break
            #if not then target slime
            if not is_targeting_slime:
                for slime in slimes:
                    if self.Checkforslime(slime) and slime[0].Canreproduce():
                        print("interupted going towards slime")
                        self.posX = slime[0].cx
                        self.posY = slime[0].cy
                        if check_collision(self.cx, self.cy, slime[0].cx, slime[0].cy):
                            partner = self.Reproduce(slime[0])
                            return partner
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
            self.posX,self.posY = self.selectlocation(slimes)

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
