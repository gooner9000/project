import Oslime
import berry
from Oslime import Slime
import random
berry_list = []
for i in range(5):
    Aberry = berry.Berry(regen_time=random.randint(400, 800),
                          available=True,
                          size=3,
                          cx=random.randint(2,  2),
                          cy=random.randint(2,  2))
    berry_list.append(Aberry)
my_slime = Slime(speed=0.2,
                    max_hunger=10,
                    current_hunger=10,
                    colour=(50,150,50),
                    size=5,
                    sight=80,
                    energy_efficiency=40,
                    cx=random.randint(5,5),
                    cy=random.randint(5,5),
                    dead=False,
                    berries=berry_list,
                    lifespan = random.randint(9000,10500))