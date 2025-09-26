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
#objects
class berry:
    def __init__(self,
                 regen_time,
                 size,
                 cx,
                 cy):
        self.regen_time = regen_time
        self.size = size
        self.cx = cx
        self.cy = cy

    #def create(self):


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
                 cy):
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


    #function to create slimes at start
    def create(self):
        pygame.draw.circle(screen,self.colour,(self.cx,self.cy),self.size)

    def selectlocation(self):
        locationX = random.randint(self.size,screen_width-self.size)
        locationY = random.randint(self.size,screen_height-self.size)

        return locationX,locationY


    def die(self):
        if self.current_hunger <= 0:
            self.kill()

    def lose_hunger(self,count):
        count += 1
        if count >= self.metabolism:
            self.die()
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










#set screen size

running = True
#control framerate
clock = pygame.time.Clock()

slimes_list = []
#set start attributes
start_size = 15
count = 0
#create slimes at start
my_slime = Slime(speed=10,
                 max_hunger=10,
                 metabolism=10,
                 current_hunger=10,
                 colour="red",
                 size=start_size,
                 sight=1,
                 agression=1,
                 cx=random.randint(start_size,screen.get_width()-start_size),
                 cy=random.randint(start_size,screen.get_height()-start_size))

my_slime2 = Slime(speed=10,
                 max_hunger=10,
                 metabolism=100,
                 current_hunger=10,
                 colour="red",
                 size=start_size,
                 sight=1,
                 agression=1,
                 cx=random.randint(start_size,screen.get_width()-start_size),
                 cy=random.randint(start_size,screen.get_height()-start_size))
#while the program is playing

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game state

    my_slime.move()
    count = my_slime.lose_hunger(count)
    print(count)


    # Drawing
    screen.fill((0, 0, 0))  # Fill screen with black
    my_slime.create()       # Draw the slime

    # Update the display
    pygame.display.flip() # Or pygame.display.update()

    # Cap the frame rate (e.g., 60 frames per second)
    clock.tick(60)

# Quit Pygame when the loop ends
pygame.quit()


