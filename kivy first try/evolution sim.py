#https://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points

#imports
import random
import pygame
import math
pygame.init()
#set screen size
screen_width = 1360
screen_height = 980
screen = pygame.display.set_mode((screen_width, screen_height))
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
#objects

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
            pygame.draw.circle(screen, 'pink', (self.cx, self.cy), self.size)
    def reset(self):






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
                 dead):
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



    #function to create slimes at start
    def create(self):

        pygame.draw.circle(screen,self.colour,(self.cx,self.cy),self.size)

    def selectlocation(self):
        locationX = random.randint(self.size,screen_width-self.size)
        locationY = random.randint(self.size,screen_height-self.size)

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

    def eat(self, berries):
        for berry in berries:
            # Check if the berry is available
            if berry.available:
                distance = calculate_distance(self.cx, self.cy, berry.cx, berry.cy)
                # If close enough to eat
                if distance < self.size + berry.size:
                    self.current_hunger += 5
                    # Cap hunger at max_hunger
                    if self.current_hunger > self.max_hunger:
                        self.current_hunger = self.max_hunger
                    berry.available = False  # The slime eats the berry
                    print(f"Yum! Hunger is now {self.current_hunger}")
                    break  # Stop checking after eating one berry per frame












#set screen size

running = True
#control framerate
clock = pygame.time.Clock()

slimes_list = []
berry_list = []
#set start attributes
start_size = 15
count = 0
#create slimes at start
my_slime = [Slime(speed=10,
                 max_hunger=10,
                 metabolism=30,
                 current_hunger=10,
                 colour="red",
                 size=start_size,
                 sight=1,
                 agression=1,
                 cx=random.randint(start_size,screen.get_width()-start_size),
                 cy=random.randint(start_size,screen.get_height()-start_size),
                 dead=False)
            ,0]

my_slime2 = [Slime(speed=10,
                 max_hunger=10,
                 metabolism=100,
                 current_hunger=10,
                 colour="blue",
                 size=start_size,
                 sight=1,
                 agression=1,
                 cx=random.randint(start_size,screen.get_width()-start_size),
                 cy=random.randint(start_size,screen.get_height()-start_size),
                 dead=False)
             ,0]
for i in range(5):
    Aberry = Berry(regen_time=0.1,
                   available=True,
                   size=100,
                   cx=random.randint(start_size,screen.get_width()-start_size),
                   cy=random.randint(start_size,screen.get_height()-start_size))
    berry_list.append(Aberry)
slimes_list.append(my_slime)
slimes_list.append(my_slime2)
#while the program is playing

while running:
    # 1. Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Update game state
    slimes_to_remove = []  # Create an empty list to hold dead slimes

    for slime_data in slimes_list:
        slime_object = slime_data[0]

        # Update the slime's state
        slime_object.eat(berry_list)
        slime_object.move()
        slime_data[1] = slime_object.lose_hunger(slime_data[1])

        # If the slime is dead, add it to our removal list
        if slime_object.dead:
            slimes_to_remove.append(slime_data)

    # 3. Now, safely remove the dead slimes AFTER the main loop is done
    for dead_slime in slimes_to_remove:
        slimes_list.remove(dead_slime)

    # 4. Drawing (this part is perfect)
    screen.fill((0, 0, 0))

    for berry in berry_list:
        berry.create()

    for slime_data in slimes_list:
        slime_data[0].create()

    # 5. Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame when the loop ends
pygame.quit()


