#https://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points

#imports
import random
import pygame
import math
import Oslime
import berry



pygame.init()
#set screen size
screen_width = 1360
screen_height = 980
screen = pygame.display.set_mode((screen_width, screen_height))
mutation_value = 0.1
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
def calculate_mutation(slime1,slime2,attribute):
    return random.randint(round(-1 * mutation_value * (slime1.attribute + slime2.attribute)),
                   round(mutation_value * (slime1.attribute + slime2.attribute)))
def Create_new_slime(slime1,slime2,berry_list,):



    speed = (slime1.speed + slime2.speed)/2 + calculate_mutation(slime1,slime2,'speed')
    max_hunger = (slime1.max_hunger + slime2.max_hunger)/2
    metabolism = (slime1.metabolism + slime2.metabolism)/2
    current_hunger = max_hunger*0.6
    colour = "purple"
    size = round((slime1.size + slime2.size)/2)
    agression = (slime1.agression + slime2.agression)/2
    sight = (slime1.sight + slime2.sight)/2
    cx = (slime1.cx + slime2.cx)/2
    cy = (slime1.cy + slime2.cy)/2
    dead = False
    berries = berry_list
    return speed,max_hunger,metabolism,current_hunger,colour,size,agression,sight,cx,cy,dead,berries

#set screen size

running = True
#control framerate
clock = pygame.time.Clock()

slimes_list = []
berry_list = []
#set start attributes
start_size = 25


count = 0

for i in range(20):
    Aberry = [berry.Berry(regen_time=500,
                   available=True,
                   size=15,
                   cx=random.randint(start_size,screen.get_width()-start_size),
                   cy=random.randint(start_size,screen.get_height()-start_size)),0]
    berry_list.append(Aberry)
#create slimes at start
for i in range(2):
    my_slime = [Oslime.Slime(speed=4,
                 max_hunger=10,
                 metabolism=100,
                 current_hunger=10,
                 colour="red",
                 size=start_size,
                 sight=200,
                 agression=1,
                 cx=random.randint(start_size,screen.get_width()-start_size),
                 cy=random.randint(start_size,screen.get_height()-start_size),
                 dead=False,
                 berries=berry_list)
             ,0]
    slimes_list.append(my_slime)
for i in range(2):
    my_slime2 = [Oslime.Slime(speed=4,
                     max_hunger=10,
                     metabolism=100,
                    current_hunger=10,
                     colour="blue",
                    size=start_size,
                     sight=200,
                     agression=1,
                     cx=random.randint(start_size,screen.get_width()-start_size),
                     cy=random.randint(start_size,screen.get_height()-start_size),
                    dead=False,
                     berries=berry_list)
                ,0]
    slimes_list.append(my_slime2)


#while the program is playing

while running:
    # 1. Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Update game state
    slimes_to_remove = []  # Create an empty list to hold dead slimes

    for slime in slimes_list:


        # Update the slime's state
        partner = slime[0].move(slimes_list)
        slime[0].eat()
        slime[0].move(slimes_list)
        slime[1] = slime[0].lose_hunger(slime[1])
        if partner is not None:
            if slime[0].Can_copy and partner.Can_copy:
                partner.Can_copy = False
                new_slime_attributes = Create_new_slime(slime[0],partner,berry_list)
                new_slime = [Oslime.Slime(speed=new_slime_attributes[0],
                     max_hunger=new_slime_attributes[1],
                     metabolism=new_slime_attributes[2],
                    current_hunger=new_slime_attributes[3],
                     colour=new_slime_attributes[4],
                    size=new_slime_attributes[5],
                     sight=new_slime_attributes[7],
                     agression=new_slime_attributes[6],
                     cx=new_slime_attributes[8],
                     cy=new_slime_attributes[9],
                    dead=new_slime_attributes[10],
                     berries=new_slime_attributes[11])
                ,0]
                slimes_list.append(new_slime)
                slime[0].current_hunger = slime[0].current_hunger * 0.6
                partner.current_hunger = partner.current_hunger * 0.6
                partner = None
        # If the slime is dead, add it to our removal list
        if slime[0].dead:
            slimes_to_remove.append(slime)

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


