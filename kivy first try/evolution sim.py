#https://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points

#imports
import random
import pygame

#objects
class Slime:
    def __init__(self,
                 speed,
                 max_hunger,
                 colour,
                 size,
                 agression,
                 cx,
                 cy):
        self.speed = speed
        self.max_hunger = max_hunger
        self.colour = colour
        self.size = size
        self.agression = agression
        self.cx = cx
        self.cy = cy
    #function to create slimes at start
    def create(self):
        pygame.draw.circle(screen,self.colour,(self.cx,self.cy),self.size)

    def selectlocation(self):
        locationX = random.randint(0,1360)
        locationY = random.randint(0,980)

        return locationX,locationY

    def move(self):
        posX,posY = self.selectlocation()
        equation = self.get_line_to(posX,posY)
        print(equation)

        #while self.cx != posX and self.cy != posY:
        self.cx += self.speed
        self.cy += equation[0]*self.cx+equation[1]


    def slope(self, PposX, PposY):
        if PposX == self.cx:
            return 0
        else:
            m = (PposY - self.cy) / (PposX - self.cx)
            return m

    def get_line_to(self, PposX, PposY):
        c = -(self.slope(PposX,PposY) * self.cx - self.cy)
        return  self.slope(PposX,PposY), c






#set screen size
screen = pygame.display.set_mode((1360, 980))
running = True

#set start attributes
start_size = 50

#create slimes at start
my_slime = Slime(0.1,
                 10,
                 "red",
                 start_size,
                 1,
                 random.randint(start_size,screen.get_width()-start_size),
                 random.randint(start_size,screen.get_height()-start_size))


#while the program is playing
while running:

    #user inputs
    for event in pygame.event.get():

        #check if user quits the program
        if event.type == pygame.QUIT:
            running = False

    #fill screen colour
    screen.fill((0, 0, 0))

    #Slime actions
    my_slime.create()
    my_slime.move()



    pygame.display.update()