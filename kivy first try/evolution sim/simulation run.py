#https://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points

#imports
import random
import pygame
import math
import slime
import berry


pygame.init()
#set screen size
screen_width = 1360
screen_height = 980
screen = pygame.display.set_mode((screen_width, screen_height))
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

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
my_slime = [slime.Slime(speed=10,
                        max_calories=10,
                        metabolism=30,
                        current_calories=10,
                        colour="red",
                        size=start_size,
                        sight=1,
                        agression=1,
                        cx=random.randint(start_size,screen.get_width()-start_size),
                        cy=random.randint(start_size,screen.get_height()-start_size),
                        dead=False)
            ,0]

my_slime2 = [slime.Slime(speed=10,
                         max_calories=10,
                         metabolism=50,
                         current_calories=10,
                         colour="blue",
                         size=start_size,
                         sight=1,
                         agression=1,
                         cx=random.randint(start_size,screen.get_width()-start_size),
                         cy=random.randint(start_size,screen.get_height()-start_size),
                         dead=False)
             ,0]
for i in range(5):
    Aberry = [berry.Berry(regen_time=500,
                   available=True,
                   size=25,
                   cx=random.randint(start_size,screen.get_width()-start_size),
                   cy=random.randint(start_size,screen.get_height()-start_size)),0]
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
    for berry_data in berry_list:
        berry_data[1] = berry_data[0].reset(berry_data[1])

    screen.fill((0, 0, 0))

    for berry_data in berry_list:
        berry_data[0].create()

    for slime_data in slimes_list:
        slime_data[0].create()

    # 5. Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame when the loop ends
pygame.quit()


