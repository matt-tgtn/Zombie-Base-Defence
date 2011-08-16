import pygame
import math
import random

class ZombieSpawner:
    '''This is a clever class to spawn and update the zombies all on it's own!
    
    It works thusly:
    
    You pass it a spawn dictionary (see below for format).
    It spawns the zombies accordingly.
    You call the update function once per frame (no args).
    It will also update the zombie sprites to make them move.
    
    Dictionary format:
    {"Zombie name":[frequency, numberZombies], 
     ... }
    
    "Zombie name": This is the name of the zombie (all lower case)
    frequency (int): This is how often to spawn the zombies (every n frames)
    numberZombies (int): Total number to spawn
    
    '''
    
    zombieTypes = ['zombie','fast']
    frame = 1
    
    def __init__(self, spawnDict, screenSize, baseLocation, screen, background):
        
        self.screenSize = screenSize
        self.baseLocation = baseLocation
        self.screen = screen
        self.background = background
        
        self.frequencies = []
        self.totalZombies = []
        self.currentTotals = []
        
        
        #Interpret the spawn dict and save it in the class
        for i in self.zombieTypes:
            if i in spawnDict:
                self.frequencies.append(spawnDict[i][0])
                self.totalZombies.append(spawnDict[i][1])
            else:
                self.frequencies.append(0)
                self.totalZombies.append(0)
            self.currentTotals.append(0)
        
        self.activeZombies = pygame.sprite.RenderUpdates()
        
    def update(self):
        
        
        #Determines whether new zombies need spawning or not
        for i in xrange(len(self.zombieTypes)):
            
            try:
                modulo = self.frame % self.frequencies[i]
            except ZeroDivisionError:
                modulo = 1
            
            if modulo==0 and self.currentTotals[i]<self.totalZombies[i]:
                if i == 0:
                    newClass = Zombie(self.screenSize, self.baseLocation)
                elif i == 1:
                    newClass = Fast(self.screenSize, self.baseLocation)
                
                
                self.activeZombies.add(newClass)
                self.currentTotals[i]+=1
                
        self.activeZombies.clear(self.screen,self.background)
        self.activeZombies.update()
        self.activeZombies.draw(self.screen)
        
        self.frame += 1      
    
    
class BaseZombie(pygame.sprite.Sprite):
    colour = [0,0,150]
    speed = 0
    health = 20
    availableScore = 100
    damagePerFrame = 0.5

    def __init__(self, screenSize, baseLocation):
        pygame.sprite.Sprite.__init__(self)
        self.screenSize = screenSize
        self.baseLocation = baseLocation
        self.pos = (0,0)
        
        
    def spawn(self):
        spawnPos = [0,0]
        
        #Determine the spawn position
        if random.randint(1,2)==1:
            if random.randint(1,2)==1:
                spawnPos[0]=self.screenSize[0]
            spawnPos[1]=random.randint(0,self.screenSize[1])
        else:
            if random.randint(1,2)==1:
                spawnPos[1]=self.screenSize[1]
            spawnPos[0]=random.randint(0,self.screenSize[0])
            
        self.pos = (spawnPos[0],spawnPos[1])    
        
        #Determine the amount to move per frame
        relx = float(self.baseLocation[0]-self.pos[0])
        rely = float(self.baseLocation[1]-self.pos[1])
        
        hypotenuse = math.sqrt((relx**2)+(rely**2))
        
        scale = float(self.speed)/hypotenuse
        
        self.xmove = scale * relx
        self.ymove = scale * rely
    
    def update(self):
        self.pos = (self.pos[0]+self.xmove,self.pos[1]+self.ymove)
        self.rect.center = self.pos
        
        if self.health <= 0:
            self.kill()
        
class Zombie(BaseZombie):

    size = [21,21]
    speed = 0.25
    health = 20
    damagePerFrame = 0.25

    def __init__(self, screenSize, baseLocation):
        BaseZombie.__init__(self, screenSize, baseLocation)
        
        self.image = pygame.surface.Surface(self.size)
        pygame.draw.circle(self.image, self.colour, [11,11], 10)
        self.image.set_colorkey([0,0,0])
        
        self.rect = self.image.get_rect()
        
        self.spawn()
        
        
class Fast(BaseZombie):

    size = [11,11]
    speed = 5
    colour = [255,0,0]

    def __init__(self, screenSize, baseLocation):
        BaseZombie.__init__(self, screenSize, baseLocation)
        
        self.image = pygame.surface.Surface(self.size)
        pygame.draw.circle(self.image, self.colour, [self.size[0]/2,self.size[1]/2], math.floor(self.size[0]/2))
        
        self.rect = self.image.get_rect()
        
        self.spawn()   
        
        
        
        
        
        
        
        
        
        
