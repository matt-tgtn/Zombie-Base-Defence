#!/usr/bin/env python
try:
    import pygame
    import os
    from pygame.locals import MOUSEBUTTONDOWN, K_ESCAPE, KEYDOWN, K_r, K_1, K_2, K_3, MOUSEBUTTONUP
    import math
    import weapons.baseguns as baseguns
    import zombies
    import labels
except ImportError:
    print 'Pygame must be installed. Please install pygame'
    
#functions used to load sounds and images (if any)
def load_image(name, colorkey=None):
    """Loads an image into memory"""
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))[:3]
        image.set_colorkey(colorkey)
    return image, image.get_rect()

def load_sound(name):
    """Loads a sound file (.wav) in memory"""
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound

######BEGIN CLASS EFINITIONS########

class Player(pygame.sprite.Sprite):

    def __init__(self, screenCentre, screen, background):
        pygame.sprite.Sprite.__init__(self)
        
        self.renderPosition = screenCentre
        self.screen = screen
        self.background = background
        
        #Initialise the guns
        self.bulletGroup = pygame.sprite.RenderUpdates()
        self.guns = []
        self.guns.append(baseguns.M9(screenCentre, self.screen, self.background, self.bulletGroup))
        self.guns.append(baseguns.SMG(screenCentre, self.screen, self.background, self.bulletGroup))
        self.guns.append(baseguns.SNIPER(screenCentre, self.screen, self.background, self.bulletGroup))
        
        self.currentGun = self.guns[0]
        self.initialImage, self.rect = load_image('player.png')
        self.initialImage.set_colorkey([255,255,255])
        self.image = self.initialImage
        
        
        self.rect.center = self.renderPosition
        
        
        

        
    def update(self, mousePosition):    
        
        
        #Establish the angle to rotate the turret by
        xdif = mousePosition[0]-self.renderPosition[0]
        ydif = mousePosition[1]-self.renderPosition[1]
        
        if not xdif == 0:
            rotationAngle = math.atan(math.fabs(ydif/float(xdif)))
            if xdif>0 and ydif>0:#Corrections for each quadrant
                pass
            elif xdif<0 and ydif>0:
                rotationAngle = (math.pi/2)+(math.pi/2-rotationAngle)
            elif xdif > 0 and ydif<0:
                rotationAngle = (3*math.pi/2)+(math.pi/2-rotationAngle)
            elif xdif<0 and ydif<0:
                rotationAngle = math.pi+rotationAngle
            #Corrections when y is equal to 0
            elif xdif>0 and ydif == 0:
                rotationAngle = 0
            elif xdif<0 and ydif == 0:
                rotationAngle = math.pi
            
            
            
            
        elif xdif == 0 and ydif > 0:
            rotationAngle = math.pi/2
        elif xdif == 0 and ydif < 0:
            rotationAngle = (3*math.pi)/2
        
        self.angle = rotationAngle
        rotationAngle = rotationAngle*(-1)
        
        self.currentGun.update()

        #Rotate the image
        self.image = pygame.transform.rotate(self.initialImage, self.ToDegrees(rotationAngle))
        self.rect = self.image.get_rect()
        self.rect.center = self.renderPosition
        
    def ToDegrees(self, radians):
        degrees = (radians/(2*math.pi))*360
        return degrees
    
    def Shoot(self, mousePos):
        self.currentGun.shoot(mousePos)



class House(pygame.sprite.Sprite):
    """The house sprite will handle the image, and allow us to manage the health (and therefore win/loss scenario)
    """
    health = 200
    
    def __init__(self, screenCentre):
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = load_image('house.png')
        self.rect.center = screenCentre

    def update(self, placeHolder):
        pass
        
        


class UpdateManager():
    """This class will initialise the elements of the game that need updating each frame and will do that when the update method is called
    """

        
    def __init__(self, screen, background, screenCentre, level):
        self.screenCentre = screenCentre
        self.screen = screen
        self.background = background

        spawnDict = self.createZombieDict(level)


        self.zombieManager = zombies.ZombieSpawner(spawnDict,screen.get_rect().size,screenCentre,screen,background)

        #Declaring the playerAsset group
        self.playerAssetGroup = pygame.sprite.OrderedUpdates()
        self.player = Player(screenCentre, screen, background)
        self.house = House(self.screenCentre)
        self.playerAssetGroup.add(self.house)
        self.playerAssetGroup.add(self.player)
        
        #Declaring the single sprite groups list and populating it accordingly
        self.singleSpriteGroups = []

        ammocounter = pygame.sprite.GroupSingle()
        ammocounter.add(labels.AmmoCounter(self.screen.get_size(), self.player.currentGun))
        self.singleSpriteGroups.append(ammocounter)

    def update(self):
        #Update the groups
        self.playerAssetGroup.clear(self.screen,self.background)
        self.playerAssetGroup.update(pygame.mouse.get_pos())
        self.playerAssetGroup.draw(self.screen)
        
        for spritegroup in self.singleSpriteGroups:
            spritegroup.clear(self.screen, self.background)
            spritegroup.update(self.player.currentGun)
            spritegroup.draw(self.screen)

                        
        self.zombieManager.update()
        
    def createZombieDict(self,level):
        spawnDict = {'zombie':[20,20]}
        #TODO: Refactor this code to actually work xD
        return spawnDict

##########END CLASS EFINITIONS#########    

def manageCollisions(UpdateManager, score):
    """
    This will detect collisions between the bullets and zombies, and also
    between zombies and the house (to determine when you lose)
    
    Arguments:
    - `UpdateManager`:
    """
    
    #Collide the bullets and zombies
    bulletGroup = UpdateManager.player.bulletGroup
    activeZombies = UpdateManager.zombieManager.activeZombies 
    collisions = pygame.sprite.groupcollide(bulletGroup, activeZombies, True, False)
    for bullet in collisions:
        for zombie in collisions[bullet]:
            zombie.health -= bullet.damage
            score += zombie.availableScore

    #Collide house and zombies
    house = UpdateManager.house
    collisions = pygame.sprite.spritecollide(house, activeZombies, False)
    for zombie in collisions:
        house.health -= zombie.damagePerFrame
        zombie.xmove = 0 #Make the zombie stop moving
        zombie.ymove = 0



    return score




def gameLoop(size, level):
    pygame.init()
    clock = pygame.time.Clock()
    
    #Create and set the screen and size
    screenSize = size
    screenCentre = [screenSize[0]/2,screenSize[1]/2]
    
    screen = pygame.display.set_mode(screenSize)
    background = pygame.Surface(screenSize)
    background.fill([150,150,0])
    screen.blit(background,[0,0])
    
    score = 0
    
    running = True
    
    #Initialise the group manager
    updateManager = UpdateManager(screen, background, screenCentre, level)
    
    shootButtonDown = False
    singleShotFired = False
    
    while running:
        clock.tick(60)
        
        #Update the sprites
        updateManager.update()
        #Manage the collisions
        score = manageCollisions(updateManager, score)

        print 'Health: %s' % updateManager.house.health
        print 'Score: %s' % (score)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    raise SystemExit()
                elif event.key == K_r:
                    updateManager.player.currentGun.reload()
                elif event.key == K_1:
                    updateManager.player.currentGun = updateManager.player.guns[0]
                    print 'Handgun active'
                elif event.key == K_2:
                    updateManager.player.currentGun = updateManager.player.guns[1]
                    print 'SMG active'
                elif event.key == K_3:
                    updateManager.player.currentGun = updateManager.player.guns[2]
                    print 'SNIPER active'
            elif event.type == MOUSEBUTTONDOWN:
                shootButtonDown = True
                singleShotFired = False
            elif event.type == MOUSEBUTTONUP:
                shootButtonDown = False
        
        #This handles the semi automatic ability of the guns
        if shootButtonDown:
            if not singleShotFired:
                updateManager.player.currentGun.shoot(pygame.mouse.get_pos())
                singleShotFired = True
            elif singleShotFired and updateManager.player.currentGun.gunType == 'auto':
                updateManager.player.currentGun.shoot(pygame.mouse.get_pos())


            
            
        
        pygame.display.flip()


def mainLoop(screenSize):
    """This is the loop that handles the progression for each phase of the game.
    
    Screen(welcome)
    |
    v
    screen(level intro) <------------
    |                               |
    v                               |
    gameLoop(level)                 |
    | ##RETURN SCORE AND HEALTH##   |
    v                               |
    screen(upgrades and ammo)-------|




    
    Arguments:
    - `screenSize`:
    """
    #Show the welcome screen here
    
    level = 1

    while True:
        #Show level intro

        gameLoop(screenSize, level)
        
        #Show upgrades screen

        level += 1


if __name__ == '__main__':
    mainLoop([500,500])
    





