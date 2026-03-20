import math
import pygame
import random


def calculate_distance(x1, y1, x2, y2):
    """ calculates the distance between two points """

    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))


def check_collision(x1, y1, x2, y2):
    """ checks if two points are close enough to be colliding"""
    if calculate_distance(x1, y1, x2, y2) <= 3:
        return True
    return False


# sets the size of the screen that the slime can use
screen_widthS = 1360
screen_heightS = 980
screenS = pygame.display.set_mode((screen_widthS, screen_heightS))


class Slime:
    """ description: class that creates and handles the slime object
        attributes: dead: is true or false slime is removed from simulation of true
                    berries: list of berries in the simulation
                    Can_copy: indicates to other slimes if is able to reproduce or not
                    speed:
                    max_hunger: used to calculate actual_max_hunger
                    energy_efficiency: set value of 40 that doesn't change, used to calculate the actual energy efficiency
                    current_hunger: amount of energy the slime currently has
                    colour: is three different 3 digit integers which make an RGB value
                    size: the radius of the slime
                    sight: the radius of the sight circle
                    cx: slimes current x position
                    cy: slimes current y position
                    posX: x position of the point the slime is moving to
                    posY: y position of the point the slime is moving to
                    lifespan: the maximum age a slime can get to before dying
                    age: how many frames a slime has been alive for
                    actual_energy_efficiency: how many frames it takes for a slime to lose 1 energy
                    actual_max_hunger: max energy a slime can have
                    """

    def __init__(self,
                 speed,
                 max_hunger,
                 energy_efficiency,
                 current_hunger,
                 colour,
                 size,
                 sight,
                 cx,
                 cy,
                 dead,
                 berries,
                 lifespan):
        self.dead = dead
        self.berries = berries
        self.Can_copy = False
        self.speed = speed
        self.max_hunger = max_hunger
        self.energy_efficiency = 40
        self.current_hunger = current_hunger
        self.colour = colour
        self.size = size
        self.sight = sight
        self.cx = cx
        self.cy = cy
        self.lifespan = lifespan
        self.age = 0
        self.actual_energy_efficiency = self.energy_efficiency / self.speed
        self.actual_max_hunger = self.max_hunger + round(self.size / 2)
        self.posX, self.posY = self.selectlocation([])

    def Increase_age(self):
        """increments the age by one everytime it is called
        also checks to see if the slime has died of old age"""
        self.age += 1
        # check if slime has died of old age
        if self.age >= self.lifespan:
            self.dead = True
            return True
        return False

    def create(self):
        """draws the slime to the screen"""
        pygame.draw.circle(screenS, self.colour, (self.cx, self.cy), self.size)

    def Ishungry(self):
        """compares current energy level to maximum energy level,
        checks if current is less than 50% of the maximum"""
        if self.current_hunger < self.actual_max_hunger * 0.5:
            return True
        else:
            return False

    def Reproduce(self, slime, debug=False):
        """sets the reproduction flag to true and identifies the partner slime"""
        self.Can_copy = True
        partner = slime
        return partner

    def Canreproduce(self):
        """checks if slime has enough energy to reproduce,
        compares current hunger to 70% of max hunger"""
        if self.current_hunger >= self.actual_max_hunger * 0.7:
            return True
        else:
            return False

    def Checkforberry(self, berry):
        """checks if a specific berry is available and within the slimes sight radius"""
        if berry[0].available:
            distance = calculate_distance(self.cx, self.cy, berry[0].cx, berry[0].cy)
            # If close enough to see
            if distance < self.sight:
                return True
        return False

    def Checkforslime(self, slime):
        """checks if another slime is within sight and ensures it is not itself"""
        distance = calculate_distance(self.cx, self.cy, slime[0].cx, slime[0].cy)
        if distance < self.sight and slime[0] is not self:
            return True
        return False

    def selectlocation(self, slimes):
        """determines the next target coordinates based on how much energy it has
        prioritizes food if hungry, then mates if able, otherwise moves randomly"""
        # set if a slime is hungry or can reproduce at the start of the function so only needs to call Ishungry and Canreproduce once
        hungry = self.Ishungry()
        repro_able = self.Canreproduce()
        # check if slime is not hungry and doesn't need to reproduce
        if not hungry and not repro_able:
            # selects a random location that is within the slimes sight circle
            locationX = self.cx + random.randint(round(-self.sight), round(self.sight))
            locationY = self.cy + random.randint(round(-self.sight), round(self.sight))
            # ensures the slime cannot select a location outside of the simulation screen
            if locationX > screen_widthS - self.size:
                locationX = screen_widthS
            if locationY > screen_heightS - self.size:
                locationY = screen_heightS
            return locationX, locationY
        # check if the slime is hungry
        elif hungry:
            # loops through the list of all berries
            for berry in self.berries:
                # check if it can see that berry
                if self.Checkforberry(berry) == True:
                    # if it can, it selects that berry's location as the next location the slime will go to
                    locationX = berry[0].cx
                    locationY = berry[0].cy
                    return locationX, locationY
            # if the slime can't see any berries, it selects a random location on the screen to go to next (searching state)
            locationX = random.randint(int(self.size), screen_widthS - int(self.size))
            locationY = random.randint(int(self.size), screen_heightS - int(self.size))
            return locationX, locationY
        # check if the slime can reproduce
        elif repro_able:
            # loops through list of all slimes
            for slime in slimes:
                # check if they can see that slime and that it can reproduce
                if self.Checkforslime(slime) == True and slime[0].Canreproduce():
                    # if it can, it selects that slimes location as the next location the slime will go to
                    locationX = slime[0].cx
                    locationY = slime[0].cy
                    # checks if the slimes are on top of eachother
                    if check_collision(self.cx, self.cy, slime[0].cx, slime[0].cy):
                        # if they are, trigger reproduction
                        self.Reproduce(slime[0])
                    return locationX, locationY
            # if no slime, enters searching state
            locationX = random.randint(int(self.size), screen_widthS - int(self.size))
            locationY = random.randint(int(self.size), screen_heightS - int(self.size))
            return locationX, locationY

    def diehunger(self):
        """checks if the slime has run out of energy and should die"""
        if self.current_hunger <= 0:
            return True
        return False

    def lose_hunger(self, count):
        """decrements hunger over time based on efficiency and checks for death"""
        #increments the frame counter by one
        count += 1
        #checks if enough frames have passed for the slime to lose energy
        if count >= self.actual_energy_efficiency:
            #if enough frames have passed reduces amount of energy by 1
            self.current_hunger -= 1
            #check if slime is starving
            if self.diehunger():
                #if is starving then trigger death
                self.dead = True
            #reset frame counter
            count = 0
        return count

    def move(self, slimes):
        """updates the slimes position and handles logic for targeting food or mates
        interrupts current path if a priority target appears in sight"""
        # check to interupt
        if self.Ishungry():
            is_targeting_food = False
            # check if already targeting food
            for berry in self.berries:
                if berry[0].available and self.posX == berry[0].cx and self.posY == berry[0].cy:
                    is_targeting_food = True
                    break
            # if not then target food
            if not is_targeting_food:
                for berry in self.berries:
                    if self.Checkforberry(berry):
                        # print("interupted going towards berry")
                        self.posX = berry[0].cx
                        self.posY = berry[0].cy
                        break
        if self.Canreproduce():
            is_targeting_slime = False
            # check if already targeting slime
            for slime in slimes:
                if self.posX == slime[0].cx and self.posY == slime[0].cy:
                    # print("is already targeting")
                    is_targeting_slime = True  # Fixed logic error in original code where this was set to is_targeting_food
                    if check_collision(self.cx, self.cy, slime[0].cx, slime[0].cy):
                        partner = self.Reproduce(slime[0])
                        return partner
                    break
            # if not then target slime
            if not is_targeting_slime:
                for slime in slimes:
                    if self.Checkforslime(slime) and slime[0].Canreproduce():
                        # print("interupted going towards slime")
                        self.posX = slime[0].cx
                        self.posY = slime[0].cy
                        if check_collision(self.cx, self.cy, slime[0].cx, slime[0].cy):
                            partner = self.Reproduce(slime[0])
                            return partner
                        break

        # calculate distance
        dx = self.posX - self.cx
        dy = self.posY - self.cy
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # If closer than one step, snap to target and pick new
        if distance < self.speed:
            wait = True
            while wait == True:
                for i in range(0, random.randint(100000, 100000)):
                    wait = False
            self.cx = self.posX
            self.cy = self.posY
            self.posX, self.posY = self.selectlocation(slimes)

        else:
            # move the circle
            if distance != 0:
                move_x = (dx / distance) * self.speed
                move_y = (dy / distance) * self.speed

                self.cx += move_x
                self.cy += move_y

    def eat(self):
        """scans for nearby berries to consume and increases hunger points
        caps hunger at the maximum limit and marks berry as unavailable"""
        for berry in self.berries:
            # Check if the berry is available
            if berry[0].available:
                distance = calculate_distance(self.cx, self.cy, berry[0].cx, berry[0].cy)
                # If close enough to eat
                if distance < self.size + berry[0].size:
                    self.current_hunger += 5
                    # Cap hunger at max_hunger
                    if self.current_hunger > self.actual_max_hunger:
                        self.current_hunger = self.actual_max_hunger
                    berry[0].available = False  # The slime eats the berry
                    # print(f"Yum! Hunger is now {self.current_hunger}")
                    break  # Stop checking after eating one berry per frame